from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from fin_project.apps.bookings.models import Booking, BookingStatus
from fin_project.apps.reviews.models import Review
from fin_project.apps.reviews.serializers import ReviewSerializer
from fin_project.apps.reviews.permissions import IsReviewAuthorOrReadOnly


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

class ReviewCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        booking_id = self.kwargs.get('booking_id')
        if booking_id:
            return Review.objects.filter(booking_id=booking_id)
        return Review.objects.none()

    def perform_create(self, serializer):
        booking_id = self.kwargs.get('booking_id')
        if not booking_id:
            raise ValidationError("booking_id is required in the URL.")

        try:
            booking = Booking.objects.get(pk=booking_id, user=self.request.user)
        except Booking.DoesNotExist:
            raise ValidationError("Invalid booking or access denied.")

        if booking.status not in [BookingStatus.CONFIRMED, BookingStatus.COMPLETED]:
            raise ValidationError("You can only leave a review for confirmed or completed bookings.")

        today = timezone.now().date()
        if today < booking.start_date:
            raise ValidationError("You can only leave a review on or after the booking start date.")

        if Review.objects.filter(user=self.request.user, booking=booking).exists():
            raise ValidationError("You have already left a review for this booking.")

        serializer.save(
            user=self.request.user,
            booking=booking,
            rental_property=booking.rental_property
        )

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related('rental_property', 'user').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewAuthorOrReadOnly]

