from rest_framework import viewsets, permissions, status
from django.contrib.gis.db.models.functions import Distance  # <-- ADDED
from django.contrib.gis.geos import Point 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import (
    Sector, Subcategory, ProviderProfile, Review, PortfolioImage,
    Message, Booking, Notification, Favorite, Report
)
from .serializers import (
    SectorSerializer, SubcategorySerializer, ProviderProfileSerializer, ReviewSerializer, PortfolioImageSerializer,
    MessageSerializer, BookingSerializer, NotificationSerializer, FavoriteSerializer, ReportSerializer
)
from accounts.permissions import IsOverallAdmin, IsServiceProvider, IsClient, IsOwner

# Core marketplace viewsets

class SectorViewSet(viewsets.ModelViewSet):
    serializer_class = SectorSerializer

    def get_queryset(self):
        queryset = Sector.objects.all()
        has_thumbnail = self.request.query_params.get('has_thumbnail')
        if has_thumbnail:
            queryset = queryset.exclude(Q(thumbnail__isnull=True) | Q(thumbnail=''))
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOverallAdmin()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['get'], url_path='subcategories')
    def subcategories(self, request, pk=None):
        sector = self.get_object()
        serializer = SubcategorySerializer(sector.subcategories.all(), many=True, context={'request': request})
        return Response(serializer.data)

class SubcategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        queryset = Subcategory.objects.select_related('sector').all()
        has_thumbnail = self.request.query_params.get('has_thumbnail')
        if has_thumbnail:
            queryset = queryset.exclude(Q(thumbnail__isnull=True) | Q(thumbnail=''))
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOverallAdmin()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['get'], url_path='providers')
    def providers(self, request, pk=None):
        subcategory = self.get_object()
        providers = ProviderProfile.objects.filter(subcategory=subcategory).select_related('user', 'sector', 'subcategory')
        serializer = ProviderProfileSerializer(providers, many=True, context={'request': request})
        return Response(serializer.data)

class ProviderProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderProfileSerializer

    def get_queryset(self):
        # Start with the base queryset including related objects.
        queryset = ProviderProfile.objects.select_related('user', 'sector', 'subcategory').prefetch_related('portfolio_images')
        
        # Filtering based on query parameters for sector, subcategory, county, subcounty, and town.
        filters = {}
        for param, field in [('sector', 'sector_id'), ('subcategory', 'subcategory_id'),
                             ('county', 'county__iexact'), ('subcounty', 'subcounty__iexact'), ('town', 'town__iexact')]:
            value = self.request.query_params.get(param)
            if value:
                filters[field] = value
        queryset = queryset.filter(**filters)

        # Location radius filter
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius')
        if lat and lng and radius:
            try:
                point = Point(float(lng), float(lat), srid=4326)
                queryset = queryset.filter(
                    location__distance_lte=(point, Distance(km=float(radius)))
                ).annotate(distance=Distance('location', point))
            except (ValueError, TypeError):
                pass

        # Text search filter
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(business_name__icontains=search) |
                Q(description__icontains=search) |
                Q(county__icontains=search) |
                Q(subcounty__icontains=search) |
                Q(town__icontains=search)
            )

        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsServiceProvider()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['get'], url_path='reviews')
    def get_reviews(self, request, pk=None):
        provider = self.get_object()
        reviews = Review.objects.filter(provider=provider, is_approved=True).select_related('client')
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='portfolio-images')
    def get_portfolio_images(self, request, pk=None):
        provider = self.get_object()
        serializer = PortfolioImageSerializer(provider.portfolio_images.all(), many=True, context={'request': request})
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.select_related('provider', 'client').all()
        provider_id = self.request.query_params.get('provider')
        is_approved = self.request.query_params.get('is_approved')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        if is_approved is not None and self.request.user.is_staff:
            queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsClient()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return [permissions.AllowAny()]

# Extended feature viewsets

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-created_at')

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.CLIENT:
            return Booking.objects.filter(client=user).order_by('-created_at')
        elif user.role == User.Role.SERVICE_PROVIDER:
            profile = getattr(user, 'providerprofile', None)
            return Booking.objects.filter(provider=profile).order_by('-created_at')
        return Booking.objects.none()

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'], url_path='mark-read')
    def mark_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"message": "Notifications marked as read."}, status=status.HTTP_200_OK)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-added_at')

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Report.objects.all().order_by('-created_at')
        return Report.objects.filter(reporter=self.request.user).order_by('-created_at')

    def get_permissions(self):
        return [permissions.IsAuthenticated()]
