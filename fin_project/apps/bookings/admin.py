from django.contrib import admin
from django.utils.html import format_html
from fin_project.apps.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "rental_property",
        "rental_type",
        "get_price_per_unit",
        "number_of_nights",
        "duration_months",
        "total_price",
        "start_date",
        "end_date",
        "colored_status",
        "created_at",
    )
    list_filter = ("status", "rental_type", "start_date", "created_at")
    search_fields = ("user__email", "rental_property__title")
    readonly_fields = (
        "number_of_nights",
        "total_price",
        "cancellation_deadline",
        "created_at",
        "updated_at",
    )
    exclude = ()

    def get_price_per_unit(self, obj):
        if obj.rental_type == obj.DAILY:
            return f"{obj.rental_property.price_per_day} / night"
        elif obj.rental_type == obj.MONTHLY:
            return f"{obj.rental_property.price_per_month} / month"
        return "—"
    get_price_per_unit.short_description = "Price per Unit"

    def colored_status(self, obj):
        color_map = {
            'pending': 'gray',
            'confirmed': 'green',
            'cancelled': 'orange',
            'completed': 'blue',
            'declined': 'red',
            'conf_cancelled': 'darkred',
        }
        color = color_map.get(obj.status, 'black')
        return format_html('<b style="color: {};">{}</b>', color, obj.get_status_display())
    colored_status.short_description = "Status"


