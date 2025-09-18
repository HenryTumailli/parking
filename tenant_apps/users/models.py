from django.db import models
from django.contrib.auth.models import User
from app.models import Client

class TenantUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[("admin","Administrador"),("operador","Operador"),("supervisor","Supervisor")],
        default="operador"
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "tenant")
