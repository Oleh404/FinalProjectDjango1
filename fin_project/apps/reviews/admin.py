from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rental_property_id', 'rating', 'created_at')
    search_fields = ('user__email', 'rental_property__title')
    list_filter = ('rating', 'created_at')