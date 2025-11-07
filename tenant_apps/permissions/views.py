from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from .serializers import PermissionSerializer
from app.authentication import TenantTokenAuthentication

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all().select_related('content_type')
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TenantTokenAuthentication]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por app si es necesario
        app_label = self.request.query_params.get('app_label', None)
        if app_label:
            queryset = queryset.filter(content_type__app_label=app_label)
        return queryset