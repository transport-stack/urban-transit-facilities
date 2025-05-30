from django.urls import include, path

from rest_framework import routers


from charges.views import OfferViewSet, ParkingSpotRateViewSet, PaymentModeViewSet

app_name = "rates"

router = routers.DefaultRouter()
# router.register("offer", OfferViewSet, basename="offer")
router.register("parkingspot", ParkingSpotRateViewSet, basename="parkingspot")
router.register("paymentmode", PaymentModeViewSet, basename="paymentmode")

urlpatterns = [
    path("", include(router.urls)),
]
