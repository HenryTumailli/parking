from rest_framework import viewsets
from .models import TenantUserProfile
from .serializers import TenantUserProfileSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from app.authentication import TenantTokenAuthentication


class TenantUserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TenantTokenAuthentication]
    queryset = TenantUserProfile.objects.all()
    serializer_class = TenantUserProfileSerializer

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)