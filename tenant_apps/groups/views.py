from rest_framework import viewsets
from .models import TenantGroup
from .serializers import TenantGroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.authentication import TenantTokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status

class TenantGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TenantTokenAuthentication]
    queryset = TenantGroup.objects.all()
    serializer_class = TenantGroupSerializer
