from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import TenantUserProfile

class TenantUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = TenantUserProfile
        fields = ["id", "username", "email", "password", "role", "tenant", "date_joined", "is_active"]
        read_only_fields = ["id", "date_joined", "is_active"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=password
        )

        profile = TenantUserProfile.objects.create(user=user, **validated_data)

        return profile
    
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
