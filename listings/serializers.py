from rest_framework import serializers
from accounts.models import User
from .models import Sector, Subcategory, ProviderProfile, Review, PortfolioImage

class SectorSerializer(serializers.ModelSerializer):
    """
    Serializer for economic sectors.
    """
    thumbnail = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Sector
        fields = ['id', 'name', 'description', 'thumbnail']


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Serializer for subcategories within a sector.
    """
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'sector', 'sector_name', 'description', 'thumbnail']


class PortfolioImageSerializer(serializers.ModelSerializer):
    """
    Serializer for provider portfolio images.
    """
    class Meta:
        model = PortfolioImage
        fields = ['id', 'image', 'caption', 'uploaded_at']


class ProviderProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for service provider profiles.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    recommended_providers = serializers.PrimaryKeyRelatedField(
        queryset=ProviderProfile.objects.all(), many=True, required=False
    )
    recommended_providers_details = serializers.SerializerMethodField()
    portfolio_images = PortfolioImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProviderProfile
        fields = [
            'id', 'user', 'business_name', 'sector', 'sector_name',
            'subcategory', 'subcategory_name', 'description', 'website', 
            'county', 'subcounty', 'town', 'verification_document',
            'is_verified', 'recommended_providers', 
            'recommended_providers_details', 'portfolio_images'
        ]

    def get_recommended_providers_details(self, obj):
        return ProviderProfileSerializer(obj.recommended_providers.all(), many=True).data

    def validate_recommended_providers(self, value):
        """
        Ensure that a provider cannot recommend themselves.
        """
        user = self.context['request'].user
        provider_profile = ProviderProfile.objects.filter(user=user).first()
        if provider_profile and provider_profile in value:
            raise serializers.ValidationError("You cannot recommend yourself.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for client reviews on service providers.
    """
    provider = serializers.PrimaryKeyRelatedField(queryset=ProviderProfile.objects.all())
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'provider', 'provider_name', 'client', 'client_name',
            'rating', 'comment', 'created_at', 'is_approved'
        ]
        read_only_fields = ['is_approved']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
