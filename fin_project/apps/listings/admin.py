from django.contrib import admin
from fin_project.apps.listings.models import RentalProperty
from django.utils.html import format_html


@admin.register(RentalProperty)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'property_type', 'description', 'rooms', 'land', 'city',
                    'zip_code', 'address', 'show_address', 'price_per_day', 'price_per_month',
                    'is_active', 'owner', 'views', 'rating', 'owner_link', "is_deleted" )
    list_per_page = 20
    list_editable = ('is_active',)
    search_fields = ('title', 'description', 'city', 'zip_code', 'category', )
    list_filter = ('category', 'property_type', 'rating', 'land', 'is_active', 'price_per_day', 'price_per_month', 'rooms')
    ordering = ('-created_at',)

    def owner_link(self, obj):
      return format_html(f'<a href="/admin/auth/user/{obj.owner.id}/">{obj.owner}</a>')
    owner_link.short_description = "Owner"

    def status_display(self, obj):
        color = "green" if obj.is_active else "red"
        return format_html('<span style="color: {};">{}</span>', color, "IS ACTIVE" if obj.is_active else "INACTIVE"
        )
    status_display.short_description = "status"

    def delete_model(self, request, obj):
        obj.soft_delete()
