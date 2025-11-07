from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import TenantUserProfile
from tenant_apps.groups.models import TenantGroup

class TenantUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name") 
    last_name = serializers.CharField(source="user.last_name")  
    password = serializers.CharField(write_only=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TenantGroup.objects.all()
    )

    class Meta:
        model = TenantUserProfile
        fields = ["id", "username", "email", "password", "first_name", "last_name","groups", "tenant", "date_joined", "is_active"]
        read_only_fields = ["id", "date_joined"]

    def validate(self, data):
        user_data = data.get("user", {})
        username = user_data.get("username")

        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "username": f"El nombre de usuario '{username}' ya existe."
            })

        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = validated_data.pop("password")
        groups_data = validated_data.pop("groups", [])

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            password=password
        )
        
        profile = TenantUserProfile.objects.create(user=user, **validated_data)
        profile.groups.set(groups_data)

        return profile
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        groups_data = validated_data.pop("groups", None)
        password = validated_data.pop("password", None) 

        # actualizar campos de User
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        # actualizar TenantUserProfile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # actualizar grupos si se envían
        if groups_data is not None:
            instance.groups.set(groups_data)

        if password:
            instance.user.set_password(password)  # actualiza password solo si se envía
        instance.user.save()

        return instance
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user_profile = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password) 
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")

        try:
            profile = TenantUserProfile.objects.get(user=user)
            profile_data = TenantUserProfileSerializer(profile).data
        except TenantUserProfile.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas")
        
        token, _ = Token.objects.get_or_create(user=user)

        return {
            "user": profile_data,
            "token": token.key
        }
