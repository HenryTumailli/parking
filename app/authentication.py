from rest_framework.authentication import TokenAuthentication
from tenant_apps.users.models import TenantUserProfile

class TenantTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            return None
        user, token = user_auth_tuple

        # tenant actual de la request
        tenant = getattr(request, 'tenant', None)
        try:
            profile = user.tenantuserprofile
        except TenantUserProfile.DoesNotExist:
            return None 

        # Usuario global puede pasar
        if profile.tenant.schema_name == "public":
            return (user, token)
        
        if profile.tenant != tenant:
            return None
        return (user, token)