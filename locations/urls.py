from django.urls import include, path
from rest_framework import routers

from locations.views import PinCodeViewSet, StateViewSet, LocationViewSet

app_name = "locations"

router = routers.DefaultRouter()
# router.register("pincode", PinCodeViewSet, basename="pincode")
# router.register("state", StateViewSet, basename="state")
router.register("location", LocationViewSet, basename="location")

urlpatterns = [
    path("", include(router.urls)),
]
