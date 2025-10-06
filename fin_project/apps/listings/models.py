from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Avg


class RentalProperty(models.Model):
    CATEGORY_CHOICES = [
        ("A", "Apartments"),
        ("H", "Houses"),
        ("C", "Commercial"),
    ]

    PROPERTY_TYPE_CHOICES = [
        ("apartment", "Apartment / Wohnung"),
        ("studio", "Studio / Studio - Wohnung"),
        ("penthouse", "Penthouse / Penthouse"),
        ("house", "House / Haus"),
        ("townhouse", "Townhouse / Reihenhaus"),
        ("villa", "Villa / Villa"),
        ("commercial space", "Commercial Space / Gewerbefläche"),
        ("office", "Office / Büro"),
        ("warehouse", "Warehouse / Lagerhaus"),
    ]

    LAND_CHOICES = [
        ("BW", "Baden-Württemberg"),
        ("BY", "Bayern"),
        ("BE", "Berlin"),
        ("BB", "Brandenburg"),
        ("HB", "Bremen"),
        ("HH", "Hamburg"),
        ("HE", "Hessen"),
        ("MV", "Mecklenburg-Vorpommern"),
        ("NI", "Niedersachsen"),
        ("NW", "Nordrhein-Westfalen"),
        ("RP", "Rheinland-Pfalz"),
        ("SL", "Saarland"),
        ("SN", "Sachsen"),
        ("ST", "Sachsen-Anhalt"),
        ("SH", "Schleswig-Holstein"),
        ("TH", "Thüringen"),
    ]


    title = models.CharField(max_length=255)
    description = models.TextField()
    land = models.CharField(max_length=30, choices=LAND_CHOICES)
    city = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=10)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=255, blank=True, null=True)
    show_address = models.BooleanField(default=False)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    rooms = models.IntegerField()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, editable=False)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)       # общее количество просмотров в list+retrieve,
                                                         # view_count подсчет просмотров в журнале
    review_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def get_property_type_display(self):
        display_name = dict(self.PROPERTY_TYPE_CHOICES).get(self.property_type, "")
        return f"{self.property_type.capitalize()} ({display_name})"

    def validate_price(self):
        if not self.price_per_day and not self.price_per_month:
            raise ValidationError("You must specify either a daily price or a monthly price!")

    def update_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = avg_rating if avg_rating else 0.0
        self.save(update_fields=['rating'])

    def update_review_count(self):
        self.review_count = self.reviews.count()
        self.save()

    def clean(self):
        self.validate_price()

    def save(self, *args, **kwargs):
        # Определение категории по типу недвижимости
        type_to_category = {
            "apartment": "A",
            "studio": "A",
            "penthouse": "A",
            "house": "H",
            "townhouse": "H",
            "villa": "H",
            "commercial space": "C",
            "office": "C",
            "warehouse": "C"
        }
        self.category = type_to_category.get(self.property_type, "")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def soft_delete(self):

        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

