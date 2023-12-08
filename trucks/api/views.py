from django.conf import settings

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from trucks import models
from trucks.api import filters, serializers

lat = openapi.Parameter(
    'lat',
    openapi.IN_QUERY,
    description='User\'s latitude',
    type=openapi.TYPE_NUMBER,
)
lon = openapi.Parameter(
    'lon',
    openapi.IN_QUERY,
    description='User\'s longitude',
    type=openapi.TYPE_NUMBER,
)
radius_m = openapi.Parameter(
    'radius_m',
    openapi.IN_QUERY,
    description=f'Radius of search in meters. Max radius is {settings.MAX_RADIUS} meters.',
    type=openapi.TYPE_INTEGER,
)


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

    @swagger_auto_schema(
        manual_parameters=[lat, lon, radius_m],
        operation_description=(
            f'Return a list of Trucks ordered by distance from given point in some radius (meters). '
            f'Max radius is {settings.MAX_RADIUS} meters.'
        ),
    )
    @action(detail=False, url_path='nearest-in-radius')
    def nearest_in_radius(self, request, *args, **kwargs):
        """Return a paginated list of Trucks with distance from given point in some radius (meters)."""
        query_params = serializers.InRadiusSerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        queryset = self.filter_queryset(self.get_queryset().within_radius(**query_params.validated_data))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
