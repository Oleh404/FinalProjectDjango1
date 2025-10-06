from rest_framework import serializers
from fin_project.apps.listings.models import RentalProperty

class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    views = serializers.SerializerMethodField()                  # общее количество просмотров в list+retrieve,
    view_count = serializers.IntegerField(read_only=True)            # view_count подсчет просмотров в журнале

    class Meta:
        model = RentalProperty
        fields =  "__all__"
        read_only_fields = ['category', 'is_active', 'created_at', 'owner']

    def get_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.owner.email
        return None

    def get_views(self, obj):
        request = self.context.get('request')
        if request and (request.user == obj.owner or request.user.is_staff):
            return obj.views
        return None

    def validate(self, data):
        price_per_day = data.get("price_per_day")
        price_per_month = data.get("price_per_month")

        if (price_per_day and price_per_day <= 0) or (price_per_month and price_per_month <= 0):
             raise serializers.ValidationError("Price must be positive!")

        if not price_per_day and not price_per_month:
             raise serializers.ValidationError("You must specify either a daily price or a monthly price!")

        return data




