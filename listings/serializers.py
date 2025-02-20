from rest_framework import serializers
from .models import Sector, Subcategory, ProviderProfile, Review

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'sector']

class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ['id', 'user', 'business_name', 'sector', 'subcategory', 'description', 'website', 'location', 'is_verified']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'provider', 'client', 'rating', 'comment', 'created_at', 'is_approved']
