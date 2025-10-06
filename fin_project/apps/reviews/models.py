from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from fin_project.apps.users.models import User
from fin_project.apps.listings.models import RentalProperty
from fin_project.apps.bookings.models import Booking

class Review(models.Model):
    rental_property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE,  related_name="reviews")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.rental_property.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.rental_property.update_rating()

