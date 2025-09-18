from rest_framework import serializers
from .models import Client,Domain

class ClientSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'created_on', 'domain']

    def create(self, validated_data):
        domain_name = validated_data.pop('domain')
        name = validated_data.get('name')
        
        tenant = Client(**validated_data)
        tenant.schema_name = name
        tenant.auto_create_schema = True
        tenant.save()

        Domain.objects.create(domain=domain_name, tenant=tenant, is_primary=True)
        return tenant