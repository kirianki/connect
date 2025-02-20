from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectorViewSet, SubcategoryViewSet, ProviderProfileViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'sectors', SectorViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'providers', ProviderProfileViewSet, basename='provider')  # Explicit basename
router.register(r'reviews', ReviewViewSet, basename='review')  # Explicit basename

urlpatterns = [
    path('', include(router.urls)),
]
