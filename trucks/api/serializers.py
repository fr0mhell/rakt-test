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
    food_items = FoodItemSerializer(source='truckfooditem_set', many=True, read_only=True)

    class Meta:
        model = models.Truck
        fields = (
            'id',
            'location_id',
            'applicant_id',
            'applicant_data',
            'facility_type',
            'location',
            'location_description',
            'schedule',
            'address',
            'blocklot',
            'block',
            'lot',
            'permit',
            'status',
            'x',
            'y',
            'days_hours',
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
