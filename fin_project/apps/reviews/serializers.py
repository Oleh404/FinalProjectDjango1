from rest_framework import serializers
from fin_project.apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='user.email', read_only=True)
    rental_property_title = serializers.StringRelatedField(source='rental_property.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'rental_property_title',
            'author',
            'rating',
            'comment',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("The rating must be from 1 to 5!")
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance