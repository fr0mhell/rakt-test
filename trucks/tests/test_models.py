from csv import DictReader

from django.test import TestCase

from trucks.management.commands.load_data import csv_row_parse_and_save
from trucks.models import Truck


class TruckTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        with open('trucks/tests/test-data.csv') as f:
            reader = DictReader(f)
            for row in reader:
                csv_row_parse_and_save(row)

        cls.truck = Truck.objects.get(location_id=1)

    def test_with_distance_self(self):
        truck = Truck.objects.filter(location_id=self.truck.location_id).with_distance(self.truck.location).first()
        self.assertEqual(truck.distance.m, 0.0)
