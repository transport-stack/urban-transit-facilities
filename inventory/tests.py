import json

from django.urls import reverse
from rest_framework import status

from locations.models import Location, LocationType
from inventory.models import FloorPlan, ParkingSpotAvailability, VehicleType
from providers.models import ServiceProvider
from accounts.models import MyUser, UserType

from rest_framework.test import APITestCase, APIClient


class InventoryAvailabilitiesTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.provider1 = ServiceProvider.objects.create(name="test_provider_1")
        self.provider2 = ServiceProvider.objects.create(name="test_provider_2")
        self.location = Location.objects.create(
            name="test_location",
            type=LocationType.METRO_STATION,
            is_parking_available=True,
            num_floors=1,
            provider=self.provider1,
        )
        self.floor = FloorPlan.objects.create(
            location=self.location,
            floor_name="test_floor",
            floor_num=1,
            num_rows=10,
            num_columns=10,
            is_parking_available=True,
            is_parking_paid=True,
        )
        self.location2 = Location.objects.create(
            name="test_location",
            type=LocationType.METRO_STATION,
            is_parking_available=True,
            num_floors=1,
            provider=self.provider2,
        )
        self.floor2 = FloorPlan.objects.create(
            location=self.location2,
            floor_name="test_floor",
            floor_num=1,
            num_rows=10,
            num_columns=10,
            is_parking_available=True,
            is_parking_paid=True,
        )
        self.vehicle_type1 = VehicleType.objects.create(
            name="test_vehicle_1", is_active=True
        )
        self.vehicle_type2 = VehicleType.objects.create(
            name="test_vehicle_2", is_active=True
        )
        self.vehicle_type3 = VehicleType.objects.create(
            name="test_vehicle_3", is_active=False
        )
        self.spot1 = ParkingSpotAvailability.objects.create(
            floor=self.floor, vehicle_type=self.vehicle_type1, total=100, available=50
        )
        self.spot2 = ParkingSpotAvailability.objects.create(
            floor=self.floor, vehicle_type=self.vehicle_type2, total=100, available=0
        )
        self.password = "test_user_pass"
        self.user = MyUser.objects.create_user(
            username="test_user",
            email="test_user@gmail.com",
            password=self.password,
            service_provider=self.provider1,
            type=UserType.SERVICE_PROVIDER,
        )

    def test_same_provider(self):
        payload = json.dumps(
            [{"vehicle_type": self.vehicle_type1.name, "available": 10}]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_other_provider(self):
        payload = json.dumps(
            [{"vehicle_type": self.vehicle_type1.name, "available": 10}]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse(
                "inventory:floorplan-availabilities", kwargs={"pk": self.floor2.pk}
            ),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_single_payload(self):
        payload = json.dumps(
            [{"vehicle_type": self.vehicle_type1.name, "available": 10}]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_multiple_payloads(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": 10},
                {"vehicle_type": self.vehicle_type2.name, "available": 10},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_inactive_vehicle_type(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": 10},
                {"vehicle_type": self.vehicle_type2.name, "available": 10},
                {"vehicle_type": self.vehicle_type3.name, "available": 10},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_invalid_vehicle_type(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": 10},
                {"vehicle_type": "some_random_name", "availability": "10"},
                {"vehicle_type": self.vehicle_type2.name, "available": 10},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        pass

    def test_zero_availability(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": 0},
                {"vehicle_type": self.vehicle_type2.name, "available": 0},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_negative_availability_single(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": -10},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        pass

    def test_negative_availability_multiple_case_1(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": -10},
                {"vehicle_type": self.vehicle_type2.name, "available": -20},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_negative_availability_multiple_case_2(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": 10},
                {"vehicle_type": self.vehicle_type2.name, "available": -20},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_negative_availability_multiple_case_3(self):
        payload = json.dumps(
            [
                {"vehicle_type": self.vehicle_type1.name, "available": -10},
                {"vehicle_type": self.vehicle_type2.name, "available": 20},
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("inventory:floorplan-availabilities", kwargs={"pk": self.floor.pk}),
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
