from rest_framework import serializers
from django.contrib.auth.models import Permission
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import TenantGroup

class TenantGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )

    class Meta:
        model = TenantGroup
        fields = ["id", "name", "tenant", "permissions"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        group = TenantGroup.objects.create(**validated_data)
        group.permissions.set(permissions)
        return group