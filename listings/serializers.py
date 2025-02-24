from rest_framework import serializers
from rest_framework_gis.fields import GeometryField  # New import for handling PointField
from accounts.models import User
from .models import (
    Sector, Subcategory, ProviderProfile, PortfolioImage, Review,
    Message, Booking, Notification, Favorite, Report
)

# Lightweight serializer for recommended providers.
class RecommendedProviderSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = ['id', 'business_name', 'sector_name', 'subcategory_name', 'is_verified']

class SectorSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Sector
        fields = ['id', 'name', 'description', 'thumbnail', 'updated_at']

class SubcategorySerializer(serializers.ModelSerializer):
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'sector', 'sector_name', 'description', 'thumbnail', 'updated_at']

class PortfolioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = ['id', 'image', 'caption', 'uploaded_at']

class ProviderProfileSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.PrimaryKeyRelatedField(read_only=True) 
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    recommended_providers = serializers.PrimaryKeyRelatedField(
        queryset=ProviderProfile.objects.all(), many=True, required=False
    )
    recommended_providers_details = serializers.SerializerMethodField()
    portfolio_images = serializers.SerializerMethodField()
    
    # New fields added
    address = serializers.CharField(required=False, allow_blank=True)
    location = GeometryField(required=False, allow_null=True)
    
    tags = serializers.CharField(required=False)
    is_featured = serializers.BooleanField(read_only=True)
    membership_tier = serializers.CharField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = [
            'id', 'user', 'business_name', 'address', 'location', 'sector', 'sector_name',
            'subcategory', 'subcategory_name', 'description', 'website', 
            'county', 'subcounty', 'town', 'verification_document',
            'is_verified', 'admin_verified_by', 'verified_at', 'tags',
            'is_featured', 'membership_tier', 'recommended_providers', 
            'recommended_providers_details', 'portfolio_images', 'updated_at'
        ]
    
    def get_recommended_providers_details(self, obj):
        return RecommendedProviderSerializer(obj.recommended_providers.all(), many=True).data

    def get_portfolio_images(self, obj):
        request = self.context.get('request')
        images = obj.portfolio_images.all()
        page_size = 5  # Customize as needed.
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        serializer = PortfolioImageSerializer(images[start:end], many=True, context=self.context)
        return serializer.data

    def validate_recommended_providers(self, value):
        user = self.context['request'].user
        provider_profile = getattr(user, 'providerprofile', None)
        if provider_profile and provider_profile in value:
            raise serializers.ValidationError("You cannot recommend yourself.")
        return value

# ... Remaining serializers unchanged ...

class ReviewSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=ProviderProfile.objects.all())
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'provider', 'provider_name', 'client', 'client_name',
            'rating', 'comment', 'created_at', 'updated_at', 'is_approved',
            'upvotes', 'downvotes'
        ]
        read_only_fields = ['is_approved', 'upvotes', 'downvotes']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

# Extended feature serializers

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Booking
        fields = ['id', 'client', 'provider', 'service_date', 'status', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'provider', 'added_at']

class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'provider', 'description', 'is_resolved', 'created_at']
        read_only_fields = ['is_resolved']
