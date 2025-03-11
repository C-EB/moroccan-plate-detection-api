from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlateDetectionViewSet

router = DefaultRouter()
router.register('plates', PlateDetectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
