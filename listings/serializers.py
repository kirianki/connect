from rest_framework import serializers
from .models import Sector, Subcategory, ProviderProfile, Review

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name']

class SubcategorySerializer(serializers.ModelSerializer):
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())  # Allow setting sector by ID

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'sector']


class ProviderProfileSerializer(serializers.ModelSerializer):
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())  # Accept sector ID
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())  # Accept subcategory ID
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Auto-assign user

    class Meta:
        model = ProviderProfile
        fields = ['id', 'user', 'business_name', 'sector', 'subcategory', 'description', 'website', 'location', 'is_verified']

class ReviewSerializer(serializers.ModelSerializer):
    provider = ProviderProfileSerializer(read_only=True)  # Nest provider details
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Auto-assign client

    class Meta:
        model = Review
        fields = ['id', 'provider', 'client', 'rating', 'comment', 'created_at', 'is_approved']

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
