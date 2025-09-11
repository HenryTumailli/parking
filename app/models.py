from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=300)
    created_on = models.DateField(auto_now_add=True)

class Domain(DomainMixin):
    pass
