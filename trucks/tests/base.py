from csv import DictReader

from trucks.management.commands.load_data import csv_row_parse_and_save


class LoadCsvMixin:

    @classmethod
    def setUpTestData(cls):
        with open('trucks/tests/test-data.csv') as f:
            reader = DictReader(f)
            for row in reader:
                csv_row_parse_and_save(row)
