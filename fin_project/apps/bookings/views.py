from django.utils import timezone

from rest_framework import generics, permissions, serializers
from fin_project.apps.bookings.models import Booking, BookingStatus
from fin_project.apps.bookings.serializers import BookingSerializer, BookingStatusSerializer
from fin_project.apps.bookings.permissions import IsBookingOwnerOrLandlord, IsLandlordOnly


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsBookingOwnerOrLandlord]

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()

        if user.is_authenticated and user.user_type == 'landlord':
            queryset = Booking.objects.filter(rental_property__owner=user)
        else:
            queryset = Booking.objects.filter(user=user)

        queryset.filter(
            status=BookingStatus.CONFIRMED,
            end_date__lt=today
        ).update(status=BookingStatus.COMPLETED)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingCancelView(generics.DestroyAPIView):    # - Cancelling of renter
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, status__in=["pending", "confirmed"])
    def perform_destroy(self, instance):
        if instance.cancellation_deadline < timezone.now().date():
            raise serializers.ValidationError("You can't cancel the booking after the cancellation deadline.")
        instance.status = "cancelled"
        instance.save()


class BookingDecisionView(generics.UpdateAPIView):     # - Decision of the property owner between 'confirmed', 'declined' or 'conf_cancelled'
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsLandlordOnly]

    def get_queryset(self):
        return Booking.objects.filter(rental_property__owner=self.request.user, status__in=["pending", "confirmed"])

    def perform_update(self, serializer):
        serializer.save()
