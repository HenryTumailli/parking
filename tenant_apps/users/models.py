from django.db import models
from django.contrib.auth.models import User
from app.models import Client
from tenant_apps.groups.models import TenantGroup

class TenantUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    groups = models.ManyToManyField(TenantGroup, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "tenant")
