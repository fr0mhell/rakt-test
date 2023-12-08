from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, mixins

from trucks import models
from trucks.api import filters, serializers


class ApplicantViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Read-only API that shows list of Applicants."""
    queryset = models.Applicant.objects.all()
    serializer_class = serializers.ApplicantSerializer
    # Omit authentication in order to focus on main features.
    permission_classes = [AllowAny, ]


class FoodItemViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Read-only API that shows list of Food Items."""
    queryset = models.FoodItem.objects.all()
    serializer_class = serializers.FoodItemSerializer
    # Omit authentication in order to focus on main features.
    permission_classes = [AllowAny, ]


class TruckViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Read-only API to show a list of Trucks filtered by different params, or search them."""
    queryset = (
        models.Truck.objects.all()
        .select_related('applicant')
        .prefetch_related('truckfooditem_set', 'truckfooditem_set__food_item')
    )
    serializer_class = serializers.TruckSerializer
    # Omit authentication in order to focus on main features.
    permission_classes = [AllowAny, ]
    filterset_class = filters.TruckFilter

    search_fields = [
        'applicant__name',
        'facility_type',
        'location_description',
        'days_hours',
        'food_items__name',
        'address',
    ]

    ordering_fields = [
        'applicant_id',
        'facility_type',
        'distance',
        'permit',
        'status',
    ]
