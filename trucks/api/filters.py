from functools import reduce
from operator import and_

from django.db.models import Q

from django_filters import (
    CharFilter,
    DateTimeFromToRangeFilter,
    Filter,
    FilterSet,
)

from trucks.models import Truck


class FoodItemsFilter(Filter):
    """Filter Trucks by FoodItem.slug values."""
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        for v in values:
            qs = qs.filter(food_items__slug=v)
        return qs


class TruckFilter(FilterSet):
    applicant_id = CharFilter(field_name='applicant_id', lookup_expr='icontains')
    facility_type = CharFilter(field_name='applicant_id', lookup_expr='icontains')
    food_items = FoodItemsFilter(field_name='food_items')
    approved = DateTimeFromToRangeFilter(field_name='approved')
    expiration_date = DateTimeFromToRangeFilter(field_name='expiration_date')

    class Meta:
        model = Truck
        fields = (
            'applicant_id',
            'facility_type',
            'food_items',
            'status',
            'approved',
            'expiration_date',
        )
