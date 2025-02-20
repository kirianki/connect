from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectorViewSet, SubcategoryViewSet, ProviderProfileViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'sectors', SectorViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'providers', ProviderProfileViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]