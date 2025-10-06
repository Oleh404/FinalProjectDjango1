import django_filters
from functools import reduce
from operator import or_
from django.db.models import Q
from fin_project.apps.listings.models import RentalProperty

class ListingFilter(django_filters.FilterSet):
    min_price_day = django_filters.NumberFilter(field_name="price_per_day", lookup_expr='gte')
    max_price_day = django_filters.NumberFilter(field_name="price_per_day", lookup_expr='lte')
    min_price_month = django_filters.NumberFilter(field_name="price_per_month", lookup_expr='gte')
    max_price_month = django_filters.NumberFilter(field_name="price_per_month", lookup_expr='lte')
    min_rooms = django_filters.NumberFilter(field_name="rooms", lookup_expr='gte')
    max_rooms = django_filters.NumberFilter(field_name="rooms", lookup_expr='lte')
    city = django_filters.CharFilter(lookup_expr="icontains")
    property_type = django_filters.CharFilter(lookup_expr='iexact')
    property_type_name = django_filters.CharFilter(field_name="property_type__name", lookup_expr="icontains")
    property_type_category = django_filters.CharFilter(field_name="property_type__category", lookup_expr="exact")
    is_active = django_filters.BooleanFilter()
    ordering = django_filters.OrderingFilter(
        fields=(
            ('price_per_day', 'price_per_day'),
            ('price_per_month', 'price_per_month'),
            ('created_at', 'created_at'),
            ('views', 'views'),
            ('reviews_total', 'reviews_total')
               ),)

    class Meta:
        model = RentalProperty
        fields = ['category', 'property_type', 'city', 'land',   'min_price_month',
                  'max_price_month', 'min_rooms', 'max_rooms']

    @property
    def qs(self):
        queryset = super().qs.filter(is_active=True)
        search_value = self.data.get("search", None)
        if search_value:
            queryset = self.custom_search(queryset, "search", search_value)
        return queryset

    def custom_search(self, queryset, field_name, value):
        search_fields = ['title', 'description', 'zip_code', 'city', 'property_type']
        queries = [Q(**{f"{field}__icontains": value}) for field in search_fields]

        if queries:
            query = reduce(or_, queries)
            return queryset.filter(query)
        return queryset









