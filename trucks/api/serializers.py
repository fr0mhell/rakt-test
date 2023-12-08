from django.conf import settings

from rest_framework import serializers

from trucks import models


class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Applicant
        fields = (
            'name',
            'slug',
        )


class FoodItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FoodItem
        fields = (
            'name',
            'slug',
        )


class TruckSerializer(serializers.ModelSerializer):
    applicant_data = ApplicantSerializer(source='applicant', read_only=True)
    food_items = FoodItemSerializer(many=True, read_only=True)
    distance_m = serializers.SerializerMethodField()

    class Meta:
        model = models.Truck
        fields = (
            'id',
            'location_id',
            'applicant_id',
            'applicant_data',
            'facility_type',
            'google_maps_url',
            'distance_m',
            'location',
            'location_description',
            'schedule',
            'days_hours',
            'food_items',
            'address',
            'blocklot',
            'block',
            'lot',
            'permit',
            'status',
            'x',
            'y',
            'noi_sent',
            'approved',
            'received',
            'prior_permit',
            'expiration_date',
            'fire_prevention_districts',
            'police_districts',
            'supervisor_districts',
            'zip_codes',
            'neighborhoods',
        )

    def get_distance_m(self, instance: models.Truck) -> float:
        if not hasattr(instance, 'distance'):
            return 0.0
        return instance.distance.m


class InRadiusSerializer(serializers.Serializer):
    """Used to validate query parameters for the `nearest_in_radius`."""
    lat = serializers.FloatField(required=True, min_value=-180, max_value=180)
    lon = serializers.FloatField(required=True, min_value=-180, max_value=180)
    radius_m = serializers.IntegerField(min_value=1, max_value=settings.MAX_RADIUS, default=settings.MAX_RADIUS)
