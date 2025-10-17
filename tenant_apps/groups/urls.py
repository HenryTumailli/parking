from .views import TenantGroupViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('api/groups',TenantGroupViewSet,'Groups tenat')

urlpatterns = [
] + router.urls