from rest_framework import viewsets, permissions
from .models import Sector, Subcategory, ProviderProfile, Review
from .serializers import SectorSerializer, SubcategorySerializer, ProviderProfileSerializer, ReviewSerializer
from accounts.permissions import IsOverallAdmin, IsSectorAdmin, IsServiceProvider, IsClient

class SectorViewSet(viewsets.ModelViewSet):
    """
    Overall admins can create, update, and delete sectors.
    Everyone else can view them.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsOverallAdmin()]
        return [permissions.AllowAny()]


class SubcategoryViewSet(viewsets.ModelViewSet):
    """
    Only overall admins can manage subcategories, but viewing is public.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsOverallAdmin()]
        return [permissions.AllowAny()]


class ProviderProfileViewSet(viewsets.ModelViewSet):
    """
    Service providers can manage their own profiles.
    Listing all service providers is public.
    """
    serializer_class = ProviderProfileSerializer
    # Removed permission_classes = [IsServiceProvider] from class level

    def get_permissions(self):
        """
        Define permissions based on action.
        - 'list' is public.
        - Other actions require IsServiceProvider or admin roles.
        """
        if self.action in ['list','retrieve']:
            return [permissions.AllowAny()]  # Publicly accessible list
        elif self.action in ['create', 'update', 'destroy']: # Include 'retrieve' if you want provider to only see their own, otherwise remove if retrieve should also be public to see individual profiles.
            return [IsServiceProvider()] # Or [IsAuthenticated()] if you want any logged in user to potentially retrieve (depending on your get_queryset logic and if you have a 'detail' view)
        else: # Potentially handle other actions if you add them. Default to IsServiceProvider for safety if unexpected actions occur.
            return [IsServiceProvider()]
        
    def get_queryset(self):
        """
        Providers see only their profile.
        Admins see all.
        Public users see all (for list view).
        """
        user = self.request.user
        if user.is_authenticated:  # Check if user is authenticated FIRST
            if user.role in ['overall_admin', 'sector_admin']:
                return ProviderProfile.objects.select_related('user', 'sector', 'subcategory').all()
            elif user.role == 'service_provider':
                return ProviderProfile.objects.filter(user=user).select_related('sector', 'subcategory')
        # Handle anonymous users:
        return ProviderProfile.objects.select_related('user', 'sector', 'subcategory').all()  # All profiles for unauthenticated users # Providers see their own

    def perform_create(self, serializer):
        """Auto-assign user to provider profile."""
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Clients can leave reviews. Anyone can read approved reviews.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Only show approved reviews unless the request user is an admin.
        """
        user = self.request.user
        if user.is_authenticated and user.role in ['overall_admin', 'sector_admin']:
            return Review.objects.select_related('provider', 'client').all()
        return Review.objects.filter(is_approved=True).select_related('provider', 'client')

    def perform_create(self, serializer):
        """Auto-assign the logged-in user as the review author (client)."""
        serializer.save(client=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsClient()]
        return super().get_permissions()
