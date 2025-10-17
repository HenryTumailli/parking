from django.contrib.auth.models import Permission
from django.db import models
from tenant_apps.users.models import Client

class TenantGroup(models.Model):
    name = models.CharField(max_length=150)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.schema_name})"