from django.db.models.signals import post_save
from django.dispatch import receiver
from fin_project.apps.bookings.models import Booking
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Booking)
def notify_owner_on_booking(sender, instance, created, **kwargs):
    if created:
        property_owner = instance.rental_property.owner
        renter = instance.user
        send_mail(
            subject='New booking',
            message=f'{renter.email} booked your property: {instance.rental_property.title}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[property_owner.email],
            fail_silently=True,
        )
