from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fin_project.apps.reviews'

    def ready(self):
        import fin_project.apps.reviews.signals
