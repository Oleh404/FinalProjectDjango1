from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

from fin_project.apps.users.models import User
from fin_project.apps.listings.models import RentalProperty


def default_cancellation_deadline(start_date=None):
    days = getattr(settings, 'CANCELLATION_DEADLINE_DAYS', 3)
    return (start_date or now().date()) - timedelta(days=days)


class BookingStatus(models.TextChoices):
    PENDING = 'pending','PENDING'
    CONFIRMED ='confirmed','CONFIRMED'
    CANCELLED ='cancelled','CANCELLED'  # 'Отменено арендатором'
    COMPLETED ='completed','COMPLETED'  # 'Завершено'
    DECLINED ='declined','DECLINED'
    CONF_CANCELLED ='conf_cancelled','CONF_CANCELLED'


class Booking(models.Model):
    DAILY = "daily"
    MONTHLY = "monthly"
    RENTAL_CHOICES = [
        (DAILY, "Daily"),
        (MONTHLY, "Monthly"),
                     ]

    rental_property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    duration_months = models.PositiveIntegerField(default=1, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    rental_type = models.CharField(max_length=10, choices=RENTAL_CHOICES, default=DAILY)
    number_of_nights = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancellation_deadline = models.DateField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def clean(self):

        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError({"end_date": "The booking end date must be later than the start date."})

        if self.rental_type == self.MONTHLY:
            if self.duration_months is None or self.duration_months < 1:
                raise ValidationError({"duration_months": "Monthly rental must be at least 1 month."})

            if self.duration_months > 24:
                self.duration_months = 24  # До 24 месяцев

            if not self.rental_property.price_per_month:
                raise ValidationError({"rental_property": "Monthly rental requires a price per month."})

        elif self.rental_type == self.DAILY:
            if not self.rental_property.price_per_day:
                raise ValidationError({"rental_property": "Daily rental requires a price per day."})

        old_status = None
        if self.pk:
            old_status = Booking.objects.get(pk=self.pk).status

        overlapping_bookings = Booking.objects.filter(
            rental_property=self.rental_property,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
            ).exclude(status__in=[
            BookingStatus.PENDING,
            BookingStatus.CANCELLED,
            BookingStatus.COMPLETED,
            BookingStatus.DECLINED,
            BookingStatus.CONF_CANCELLED,
        ])

        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)  # Исключаем себя

        if overlapping_bookings.exists() and not (old_status == "CONFIRMED" and self.status == "CONF_CANCELLED"):
            raise ValidationError("This property is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        self.clean()

        if self.rental_type == self.DAILY:
            self.duration_months = None
            if self.start_date and self.end_date:
                self.number_of_nights = max((self.end_date - self.start_date).days, 0)
                self.total_price = self.number_of_nights * (
                    self.rental_property.price_per_day if self.rental_property else 0)

        elif self.rental_type == self.MONTHLY:
            if self.start_date and self.duration_months:
                if self.duration_months < 1 or self.duration_months > 24:
                    raise ValidationError("Rental duration must be between 1 and 24 months.")

                self.end_date = self.start_date + relativedelta(months=self.duration_months)
                price = self.rental_property.price_per_month or 0
                self.total_price = self.duration_months * price

        if not self.cancellation_deadline:
            days = getattr(settings, 'CANCELLATION_DEADLINE_DAYS', 3)
            self.cancellation_deadline = self.start_date - timedelta(days=days)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.rental_property} ({self.status})"

    class Meta:
        verbose_name = "Booking"
        ordering = ['-created_at']



