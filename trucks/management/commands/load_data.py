from typing import Any

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from trucks import models
from decimal import Decimal
import datetime as dt
from logging import getLogger
from csv import DictReader

logger = getLogger(__name__)


def csv_row_parse_and_save(row: dict[str, Any]):
    """Simple parsing and conversion of row data to save into DB."""
    location_id = row['locationid']

    applicant_name = row['Applicant']
    applicant_slug = slugify(applicant_name)

    facility_type = row['FacilityType']
    cnn = row['cnn']
    location_description = row['LocationDescription']
    address = row['Address']
    blocklot = row['blocklot'] or ''
    block = row['block'] or ''
    lot = row['lot'] or ''
    permit = row['permit'] or ''
    status = row['Status']
    x = Decimal(row['X']) if row['X'] else None
    y = Decimal(row['Y']) if row['Y'] else None
    latitude = Decimal(row['Latitude'])
    longitude = Decimal(row['Longitude'])
    schedule = row['Schedule']
    days_hours = row['dayshours'] or ''
    noi_sent = row['NOISent'] or ''
    approved = dt.datetime.strptime(row['Approved'], '%m/%d/%Y %I:%M:%S %p') if row['Approved'] else None
    received = dt.datetime.strptime(row['Received'], '%Y%m%d').date() if row['Received'] else None
    prior_permit = int(row['PriorPermit'])
    expiration_date = dt.datetime.strptime(row['ExpirationDate'], '%m/%d/%Y %I:%M:%S %p') if row['ExpirationDate'] else None
    fire_prevention_districts = int(row['Fire Prevention Districts']) if row['Fire Prevention Districts'] else None
    police_districts = int(row['Police Districts']) if row['Police Districts'] else None
    supervisor_districts = int(row['Supervisor Districts']) if row['Supervisor Districts'] else None
    zip_codes = int(row['Zip Codes']) if row['Zip Codes'] else None
    neighborhoods = int(row['Neighborhoods (old)']) if row['Neighborhoods (old)'] else None

    if not (applicant := models.Applicant.objects.filter(slug=applicant_slug).first()):
        try:
            applicant = models.Applicant.objects.create(name=applicant_name, slug=applicant_slug)
        except Exception as e:
            logger.error('Failed to create Applicant. Error: %s', e)

    # In a few lines wrong separator (;) was used
    food_items: list[models.FoodItem] = []
    for item_line in row['FoodItems'].replace('; ', ': ').split(': '):
        item_slug = slugify(item_line)

        if not (food_item := models.FoodItem.objects.filter(slug=item_slug).first()):
            try:
                food_item = models.FoodItem.objects.create(name=item_line, slug=item_slug)
            except Exception as e:
                logger.error('Failed to create FoodItem. Error: %s', e)
        food_items.append(food_item)

    truck = models.Truck.objects.create(
        location_id=location_id,
        applicant=applicant,
        facility_type=facility_type,
        cnn=cnn,
        location_description=location_description,
        address=address,
        blocklot=blocklot,
        block=block,
        lot=lot,
        permit=permit,
        status=status,
        x=x,
        y=y,
        location=Point((longitude, latitude)),
        schedule=schedule,
        days_hours=days_hours,
        noi_sent=noi_sent,
        approved=approved,
        received=received,
        prior_permit=prior_permit,
        expiration_date=expiration_date,
        fire_prevention_districts=fire_prevention_districts,
        police_districts=police_districts,
        supervisor_districts=supervisor_districts,
        zip_codes=zip_codes,
        neighborhoods=neighborhoods,
    )

    for food_item in food_items:
        try:
            models.TruckFoodItem.objects.create(truck=truck, food_item=food_item)
        except Exception as e:
            logger.error('Failed to create TruckFoodItem. Error: %s', e)

    logger.info('Truck %s created', truck)


class Command(BaseCommand):
    help = "Load food truck data from CSV file into database."

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file) as f:
            reader = DictReader(f)
            for row in reader:
                csv_row_parse_and_save(row)
