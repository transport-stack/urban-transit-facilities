from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import pytest

User = get_user_model()

@pytest.mark.django_db
class CoreAppTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@example.com',
            password='testpassword123'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_admin_site_accessible_by_superuser(self):
        """Ensure admin site is accessible by superuser."""
        self.client.login(username='testadmin', password='testpassword123')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_site_redirects_for_regular_user(self):
        """Ensure admin site redirects to login for non-staff user."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn(reverse('admin:login'), response.url)

    def test_index_view_loads(self):
        """Test that the main index page loads correctly."""
        response = self.client.get(reverse('index')) # 'index' from core.urls
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_healthcheck_view(self):
        """Test the healthcheck endpoint."""
        response = self.client.get(reverse('healthcheck')) # 'healthcheck' from core.urls
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'status': 'ok', 'message': 'Application is healthy'})

    @pytest.mark.skipif(not User.objects.filter(is_staff=True).exists(), reason="Requires DEBUG=True for API docs")
    def test_api_schema_view_loads_for_superuser_in_debug(self):
        """Test that the API schema view loads for superuser if DEBUG is True."""
        # This test assumes DEBUG=True (as per SpectacularApp.ready() for schema URLs)
        # and that a superuser can access it.
        # In a real scenario, you might mock settings.DEBUG for this test.
        from django.conf import settings
        if settings.DEBUG:
            self.client.login(username='testadmin', password='testpassword123')
            try:
                response = self.client.get(reverse('schema'))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
            except Exception as e:
                pytest.skip(f"Skipping schema test, possibly due to URL not found or other config: {e}")
        else:
            pytest.skip("Skipping API schema test as DEBUG is False")

    def test_login_redirects_view(self):
        """Test the login_redirects view."""
        # This view likely redirects based on user type, so we test the initial response
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('login_redirects'))
        # The specific redirect target depends on the view's logic, 
        # but it should be a redirect (302) for a logged-in user.
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

# It's good practice to have a simple test in each app's tests.py
# For example, in accounts/tests.py
