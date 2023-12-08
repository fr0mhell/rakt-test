from django.test import TestCase

from trucks.api.filters import FoodItemsFilter
from trucks.models import Truck
from trucks.tests.base import LoadCsvMixin


class TestFilters(LoadCsvMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.filter = FoodItemsFilter()

    def test_filter_by_food_items(self):
        params = [
            ('burritos', 2),
            ('burritos,tacos', 1),
            ('burritos,hotdogs', 1),
            ('burritos,hotdogs,tacos', 0),
        ]

        for food_items, expected_count in params:
            with self.subTest(food_items=food_items):
                qs = self.filter.filter(qs=Truck.objects.all(), value=food_items)
                self.assertEqual(qs.count(), expected_count)

