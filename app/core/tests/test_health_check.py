"""Health checkup Test"""

from django.test import TestCase

from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


class HealthCheckTests(TestCase):

    def test_health_check(self):
        self.client = APIClient()
        url = reverse('health-check')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)



