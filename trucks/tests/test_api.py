from django.urls import reverse

from rest_framework.test import APITestCase

from trucks.tests.base import LoadCsvMixin


class TestTruckApi(LoadCsvMixin, APITestCase):

    def test_nearest_in_radius(self):
        """Check computations applied correctly via API call."""
        lat = 37.78
        lon = -122.40

        radius_m = 1000
        expected_truck_ids = [1]

        with self.subTest(radius_m=radius_m):
            response = self.client.get(
                reverse('trucks-nearest-in-radius'),
                {'lat': lat, 'lon': lon, 'radius_m': radius_m},
            )
            self.assertEqual(response.status_code, 200, response.data)
            data = response.data['results']
            self.assertEqual(len(data), len(expected_truck_ids))
            self.assertListEqual([truck['id'] for truck in data], expected_truck_ids)
