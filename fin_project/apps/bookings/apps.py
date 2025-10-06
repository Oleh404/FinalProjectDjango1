from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fin_project.apps.bookings'

    def ready(self):
        import fin_project.apps.bookings.signals
