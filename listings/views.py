from rest_framework import viewsets, permissions
from .models import Sector, Subcategory, ProviderProfile, Review
from .serializers import SectorSerializer, SubcategorySerializer, ProviderProfileSerializer, ReviewSerializer
from accounts.permissions import IsOverallAdmin, IsSectorAdmin, IsServiceProvider, IsClient

class SectorViewSet(viewsets.ModelViewSet):
    """
    Overall admins can create sectors.
    Sector admins can only view sectors.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsOverallAdmin()]
        return [permissions.AllowAny()]


class SubcategoryViewSet(viewsets.ModelViewSet):
    """
    Only overall admins can create subcategories.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsOverallAdmin]


class ProviderProfileViewSet(viewsets.ModelViewSet):
    """
    Service providers can manage their own profiles.
    """
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsServiceProvider()]
        return [permissions.AllowAny()]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Only clients can leave reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsClient()]
        return [permissions.AllowAny()]
