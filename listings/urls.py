from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SectorViewSet,
    SubcategoryViewSet,
    ProviderProfileViewSet,
    ReviewViewSet
)
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'providers', ProviderProfileViewSet, basename='provider')
router.register(r'reviews', ReviewViewSet, basename='review')

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include all router-generated URLs

    # Custom actions for filtering and additional functionality
    path('sectors/<int:pk>/subcategories/', SectorViewSet.as_view({'get': 'subcategories'}), name='sector-subcategories'),
    path('subcategories/<int:pk>/providers/', SubcategoryViewSet.as_view({'get': 'providers'}), name='subcategory-providers'),
    path('providers/<int:pk>/reviews/', ProviderProfileViewSet.as_view({'get': 'get_reviews'}), name='provider-reviews'),
    path('providers/<int:pk>/portfolio-images/', ProviderProfileViewSet.as_view({'get': 'get_portfolio_images'}), name='provider-portfolio-images'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
