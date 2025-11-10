from rest_framework import viewsets
from .models import TenantUserProfile
from .serializers import TenantUserProfileSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.authentication import TenantTokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status


class TenantUserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TenantTokenAuthentication]
    queryset = TenantUserProfile.objects.all().order_by('user__username')
    serializer_class = TenantUserProfileSerializer

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TenantTokenAuthentication]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(
            {"detail": "Sesión cerrada correctamente"},
            status=status.HTTP_200_OK
        )