from functools import reduce
from operator import and_

from django.db.models import Q

from django_filters import (
    CharFilter,
    DateTimeFromToRangeFilter,
    Filter,
    FilterSet,
    NumberFilter,
)

from trucks.models import Truck


class FoodItemsFilter(Filter):
    """Filter Trucks by FoodItem.slug values."""
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        qs = qs.filter(reduce(and_, [Q(food_items__slug=v) for v in values]))
        return qs


class TruckFilter(FilterSet):
    applicant_id = CharFilter(field_name='applicant_id', lookup_expr='icontains')
    facility_type = CharFilter(field_name='applicant_id', lookup_expr='icontains')
    food_items = FoodItemsFilter(field_name='food_items')
    status = CharFilter(field_name='status', lookup_expr='icontains')
    approved = DateTimeFromToRangeFilter(field_name='approved')
    expiration_date = DateTimeFromToRangeFilter(field_name='expiration_date')
    max_distance = NumberFilter(field_name='distance_m', lookup_expr='lte')

    class Meta:
        model = Truck
        fields = (
            'applicant_id',
            'facility_type',
            'food_items',
            'status',
            'approved',
            'expiration_date',
            'max_distance',
        )
