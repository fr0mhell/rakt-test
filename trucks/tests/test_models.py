from django.test import TestCase

from trucks.models import Truck
from trucks.tests.base import LoadCsvMixin


class TruckTestCase(LoadCsvMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.truck = Truck.objects.get(location_id=1)

    def test_in_radius_self(self):
        params = {'lat': self.truck.location.y, 'lon': self.truck.location.x, 'radius_m': 0}
        truck = Truck.objects.filter(location_id=self.truck.location_id).in_radius(**params).first()
        self.assertEqual(truck.distance.m, 0.0)

    def test_in_radius(self):
        lat = 37.78
        lon = -122.40

        sub_test_params = [
            dict(
                radius_m=1000,
                expected_distances=[878.55628585],
            ),
            dict(
                radius_m=2000,
                expected_distances=[878.55628585, 1492.10260033, 1635.50164962, 1956.5667147],
            ),
            dict(
                radius_m=10_000,
                expected_distances=[878.55628585, 1492.10260033, 1635.50164962, 1956.5667147, 7016.5160145],
            ),
        ]
        for params in sub_test_params:
            radius_m = params['radius_m']
            expected_distances = params['expected_distances']
            with self.subTest(radius_m=radius_m):
                trucks = Truck.objects.in_radius(lat=lat, lon=lon, radius_m=radius_m).order_by('distance')
                distances = [truck.distance.m for truck in trucks]
                self.assertEqual(len(distances), len(expected_distances))
                self.assertListEqual(distances, expected_distances)
