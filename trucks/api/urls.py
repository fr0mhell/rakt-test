from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('applicants', views.ApplicantViewSet, basename='applicants')
router.register('food-items', views.FoodItemViewSet, basename='food-items')
router.register('trucks', views.TruckViewSet, basename='trucks')

urlpatterns = router.urls
