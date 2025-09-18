from rest_framework import viewsets
from .models import TenantUserProfile
from .serializers import TenantUserProfileSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class TenantUserProfileViewSet(viewsets.ModelViewSet):
    queryset = TenantUserProfile.objects.all()
    serializer_class = TenantUserProfileSerializer

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)