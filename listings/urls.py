from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SectorViewSet, SubcategoryViewSet, ProviderProfileViewSet, ReviewViewSet,
    MessageViewSet, BookingViewSet, NotificationViewSet, FavoriteViewSet, ReportViewSet
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'providers', ProviderProfileViewSet, basename='provider')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
