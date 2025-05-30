import json

from django.urls import reverse
from rest_framework import status

from providers.models import ServiceProvider
from accounts.models import MyUser, UserType

from rest_framework.test import APITestCase, APIClient


class MyUserTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.provider1 = ServiceProvider.objects.create(name="test_provider_1")
        self.password = "test_user_pass"
        self.user = MyUser.objects.create_user(
            username="test_user",
            email="test_user@gmail.com",
            password=self.password,
            service_provider=self.provider1,
            type=UserType.SERVICE_PROVIDER,
        )

    def test_login(self):
        payload = json.dumps(
            {"username": self.user.username, "password": self.password}
        )
        response = self.client.post(
            reverse("accounts:token_obtain_pair"),
            payload,
            content_type="application/json",
        )
        self.assertEqual(self.user.type, UserType.SERVICE_PROVIDER)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
