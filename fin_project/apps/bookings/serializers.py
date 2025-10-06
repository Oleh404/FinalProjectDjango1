from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from fin_project.apps.bookings import permissions
from fin_project.apps.bookings.models import Booking, BookingStatus
from fin_project.apps.users.models import User


class BookingSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'total_price']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.rental_type == "monthly":
            data.pop("number_of_nights", None)
        return data

    def validate(self, data):
        today = timezone.now().date()
        start_date = data['start_date']
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.date()
            data['start_date'] = start_date

        rental_type = data.get("rental_type")
        listing = data.get("rental_property")

        if rental_type == Booking.MONTHLY and not listing.price_per_month:
            raise serializers.ValidationError({
                "rental_property": "Monthly rental requires a price per month."
            })
        if rental_type == Booking.DAILY and not listing.price_per_day:
            raise serializers.ValidationError({
                "rental_property": "Daily rental requires a price per day."
            })

        if rental_type == Booking.MONTHLY:
            if "duration_months" not in data:
                raise serializers.ValidationError({"duration_months": "Required for monthly rental."})

            if "start_date" in data and "duration_months" in data:
                data["end_date"] = data["start_date"] + relativedelta(months=data["duration_months"])

        elif rental_type == Booking.DAILY:
            if "end_date" not in data:
                raise serializers.ValidationError({"end_date": "Required for daily rental."})

        end_date = data['end_date']
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()

        if start_date < today:
            raise serializers.ValidationError("Start date must be in the future!")

        if end_date <= start_date:
            raise serializers.ValidationError("The end date must be later than the start date!")

        overlapping_bookings = Booking.objects.filter(
            rental_property=data['rental_property'],
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exclude(id=self.instance.id if self.instance else None)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("These dates are already taken!")

        return data


class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']

    def validate_status(self, value):
        if value not in [
            BookingStatus.CONFIRMED,
            BookingStatus.DECLINED,
            BookingStatus.CONF_CANCELLED,
        ]:
            raise serializers.ValidationError(
                "Invalid status. Choose either 'confirmed', 'declined' or 'conf_cancelled'."
            )
        return value

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance
