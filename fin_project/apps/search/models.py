from django.db import models
from fin_project.apps.users.models import User
from fin_project.apps.listings.models import RentalProperty


class SearchHistoryManager(models.Manager):
    def get_popular_queries(self, days=None, limit=10):
        queryset = self.get_queryset()
        if days:
            from django.utils import timezone
            from datetime import timedelta
            date_threshold = timezone.now() - timedelta(days=days)
            queryset = queryset.filter(created_at__gte=date_threshold)

        return queryset.values('query').annotate(
            count=models.Count('id')
        ).order_by('-count')[:limit]

    def get_user_recent_searches(self, user, limit=5):
        return self.filter(user=user).order_by('-created_at')[:limit]


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    objects = SearchHistoryManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Search Histories'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['query']),
        ]

    def __str__(self):
        user_email = self.user.email if self.user else "Anonymous"
        return f"{user_email} searched for {self.query}"


class ViewHistoryManager(models.Manager):
    def get_popular_listings(self, days=None, limit=10):
        queryset = self.get_queryset()
        if days:
            from django.utils import timezone
            from datetime import timedelta
            date_threshold = timezone.now() - timedelta(days=days)
            queryset = queryset.filter(viewed_at__gte=date_threshold)

        return queryset.values('listing').annotate(
            count=models.Count('id')
        ).order_by('-count')[:limit]


class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    listing = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name="viewhistory")
    viewed_at = models.DateTimeField(auto_now_add=True)
    objects = ViewHistoryManager()

    class Meta:
        ordering = ['-viewed_at']
        verbose_name_plural = 'View Histories'
        indexes = [
            models.Index(fields=['user', 'viewed_at']),
            models.Index(fields=['listing']),
        ]

    def __str__(self):
        user_email = self.user.email if self.user else "Anonymous"
        return f"{user_email} viewed {self.listing.title}"
