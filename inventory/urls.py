from django.urls import include, path, reverse

from rest_framework import routers
from inventory.views import (
    FloorPlanViewSet,
    ParkingSpotViewSet,
    VehicleTypeViewSet,
    FloorPlanPredictionViewSet,
)

app_name = "inventory"

router = routers.DefaultRouter()
router.register("floorplan", FloorPlanViewSet, basename="floorplan")
# router.register("parkingspot", ParkingSpotViewSet, basename="parkingspot")
router.register("vehicletype", VehicleTypeViewSet, basename="vehicletype")
router.register("prediction", FloorPlanPredictionViewSet, basename="prediction")

urlpatterns = [
    path("", include(router.urls)),
]
