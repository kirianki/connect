from django.contrib import admin
from .models import Sector, Subcategory, ProviderProfile, Review

admin.site.register(Sector)
admin.site.register(Subcategory)
admin.site.register(ProviderProfile)
admin.site.register(Review)
