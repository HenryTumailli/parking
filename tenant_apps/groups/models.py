from django.contrib.auth.models import Permission
from django.db import models
from tenant_apps.users.models import Client

class TenantGroup(models.Model):
    name = models.CharField(max_length=150,unique=True,verbose_name="Nombre")
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.schema_name})"
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"