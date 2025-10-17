from django.urls import path
from django.contrib import admin
from rest_framework import routers
from .views import TenantUserProfileViewSet
from .views import LoginView,LogoutView

router = routers.DefaultRouter()
router.register('api/users',TenantUserProfileViewSet,'Users tenat')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + router.urls