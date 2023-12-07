from rest_framework.viewsets import mixins, GenericViewSet
from trucks.api import serializers
from trucks import models
from rest_framework.permissions import AllowAny


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
    queryset = models.Truck.objects.all()
    serializer_class = serializers.TruckSerializer
    # Omit authentication in order to focus on main features.
    permission_classes = [AllowAny, ]
