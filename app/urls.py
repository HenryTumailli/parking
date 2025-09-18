from django.urls import path
from django.contrib import admin
from rest_framework import routers
from .views import ClientViewSet

router = routers.DefaultRouter()
router.register('api/clients',ClientViewSet,'Clientes')

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls