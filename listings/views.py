from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sector, Subcategory, ProviderProfile, Review, PortfolioImage
from .serializers import (
    SectorSerializer,
    SubcategorySerializer,
    ProviderProfileSerializer,
    ReviewSerializer,
    PortfolioImageSerializer
)
from accounts.permissions import IsOverallAdmin, IsServiceProvider, IsClient, IsOwner


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOverallAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = self.queryset
        has_thumbnail = self.request.query_params.get('has_thumbnail')
        if has_thumbnail:
            queryset = queryset.exclude(thumbnail='')
        return queryset

    @action(detail=True, methods=['get'], url_path='subcategories')
    def subcategories(self, request, pk=None):
        sector = self.get_object()
        subcategories = sector.subcategories.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all().select_related('sector')
    serializer_class = SubcategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOverallAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = self.queryset
        has_thumbnail = self.request.query_params.get('has_thumbnail')
        if has_thumbnail:
            queryset = queryset.exclude(thumbnail='')
        return queryset

    @action(detail=True, methods=['get'], url_path='providers')
    def providers(self, request, pk=None):
        subcategory = self.get_object()
        providers = ProviderProfile.objects.filter(subcategory=subcategory).select_related('user', 'sector', 'subcategory')
        serializer = ProviderProfileSerializer(providers, many=True)
        return Response(serializer.data)


class ProviderProfileViewSet(viewsets.ModelViewSet):
    queryset = ProviderProfile.objects.all().select_related('user', 'sector', 'subcategory')
    serializer_class = ProviderProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsServiceProvider()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = self.queryset
        sector_id = self.request.query_params.get('sector')
        subcategory_id = self.request.query_params.get('subcategory')
        county = self.request.query_params.get('county')
        subcounty = self.request.query_params.get('subcounty')
        town = self.request.query_params.get('town')

        if sector_id:
            queryset = queryset.filter(sector_id=sector_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        if county:
            queryset = queryset.filter(county__iexact=county)
        if subcounty:
            queryset = queryset.filter(subcounty__iexact=subcounty)
        if town:
            queryset = queryset.filter(town__iexact=town)

        return queryset

    @action(detail=True, methods=['get'], url_path='reviews')
    def get_reviews(self, request, pk=None):
        provider = self.get_object()
        reviews = Review.objects.filter(provider=provider, is_approved=True).select_related('client')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='portfolio-images')
    def get_portfolio_images(self, request, pk=None):
        provider = self.get_object()
        images = PortfolioImage.objects.filter(provider=provider)
        serializer = PortfolioImageSerializer(images, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('provider', 'client')
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsClient()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = self.queryset
        provider_id = self.request.query_params.get('provider')
        is_approved = self.request.query_params.get('is_approved')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        if is_approved is not None:
            queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
        return queryset
