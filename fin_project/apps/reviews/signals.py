from django.db.models.signals import post_save
from django.dispatch import receiver
from fin_project.apps.reviews.models import Review
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Review)
def notify_owner_on_review(sender, instance, created, **kwargs):
    if created:
        property_owner = instance.booking.rental_property.owner
        reviewer = instance.user
        send_mail(
            subject='New review',
            message=f'{reviewer.email} left a review for your property: {instance.booking.rental_property.title}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[property_owner.email],
            fail_silently=True,
        )
