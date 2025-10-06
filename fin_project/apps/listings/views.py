from rest_framework import generics, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Count

from fin_project.apps.listings.models import RentalProperty
from fin_project.apps.listings.serializers import PropertySerializer
from fin_project.apps.listings.permissions import IsOwnerOrReadOnly
from fin_project.apps.listings.filters import ListingFilter
from fin_project.apps.search.models import SearchHistory, ViewHistory

class ListingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = RentalProperty.objects.filter(is_active=True)
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ListingPagination
    filterset_class = ListingFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price_per_day', 'price_per_month', 'created_at']
    ordering = []
    search_fields = ['title__icontains', 'description__icontains', 'city__icontains', 'zip_code__icontains']

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR')

    def perform_search(self, query):
        if query:
            user = self.request.user if self.request.user.is_authenticated else None
            ip = self.get_client_ip()
            SearchHistory.objects.create(user=user, query=query, ip_address=ip)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in self.paginate_queryset(self.get_queryset()):
            RentalProperty.objects.filter(pk=item.pk).update(views=F('views') + 1)
        return response

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            reviews_total=Count('reviews')
        )
        search_query = self.request.GET.get("search")
        if search_query:
            self.perform_search(search_query)

        ordering_param = self.request.GET.get('ordering', '-created_at')
        if ordering_param in ['price_per_day', '-price_per_day', 'created_at', '-created_at']:
            return queryset.order_by(ordering_param)
        return queryset.order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RentalProperty.objects.filter(is_deleted=False)
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "property_type", "price_per_day", "price_per_month"]

    def perform_destroy(self, instance):
        instance.soft_delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        RentalProperty.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        instance.refresh_from_db(fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        obj = super().get_object()
        ViewHistory.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            listing=obj)
        return obj


class PropertyToggleStatusView(generics.UpdateAPIView):
    queryset = RentalProperty.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        property_obj = self.get_object()
        if property_obj.owner != request.user:
            return Response({'detail': "No access!"}, status=status.HTTP_403_FORBIDDEN)
        property_obj.is_active = not property_obj.is_active
        property_obj.save()
        return Response({'status': 'updated', 'is_active': property_obj.is_active})
