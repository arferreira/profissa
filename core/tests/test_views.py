from django.test import TestCase
from django.urls import reverse


class LandingProviderTestCase(TestCase):

    def test_landing_provider_status_code(self):
        url = reverse('landing:provider')
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)
