from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from fin_project.apps.listings.models import RentalProperty
from fin_project.apps.listings.serializers import PropertySerializer
from fin_project.apps.search.models import SearchHistory


class SearchView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def perform_search(self, query):
        print(">>> perform_search вызван")
        if query:
            user = self.request.user if self.request.user.is_authenticated else None
            ip = self.get_client_ip()
            print(f"[SEARCH] Query: '{query}', User: {user}, IP: {ip}")
            SearchHistory.objects.create(user=user, query=query, ip_address=ip)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        print(f">>> IP определён как: {ip}")
        return ip

    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        print(f"--> Получен параметр search: '{query}'")  # DEBUG
        self.perform_search(query)
        return RentalProperty.objects.filter(is_active=True).search(query)


class PopularListingsView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        days = self.request.GET.get("days", 30)

        try:
            days = int(days)
        except ValueError:
            days = 30

        date_threshold = timezone.now() - timedelta(days=days)

        queryset = RentalProperty.objects.filter(
            is_active=True,
            viewhistory__viewed_at__gte=date_threshold
        ).annotate(
            view_count=Count('viewhistory')
        ).order_by('-view_count')

        return queryset.distinct()[:10]


class PopularSearchesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        days = request.GET.get('days')
        limit = request.GET.get('limit', 10)

        try:
            days = int(days) if days else None
            limit = int(limit)
        except ValueError:
            return Response({'error': 'Invalid parameters'}, status=400)

        popular_searches = SearchHistory.objects.get_popular_queries(days=days, limit=limit)
        return Response(popular_searches)

