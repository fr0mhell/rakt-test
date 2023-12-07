from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.text import slugify


class NameAndSlugModel(models.Model):
    """Model that stores entities with unique names.

    Use slug to guarantee uniqueness of name.

    """
    name = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=1024, primary_key=True, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)


class Applicant(NameAndSlugModel):
    ...


class FoodItem(NameAndSlugModel):
    ...


class Truck(models.Model):
    location_id = models.IntegerField()
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    facility_type = models.CharField(max_length=255)
    cnn = models.IntegerField()
    location_description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    blocklot = models.CharField(max_length=20, blank=True)
    block = models.CharField(max_length=20, blank=True)
    lot = models.CharField(max_length=20, blank=True)
    permit = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, blank=True)
    food_items = models.TextField(blank=True)
    x = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    y = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    location = gis_models.PointField(null=True, blank=True)
    schedule = models.TextField(blank=True)
    days_hours = models.TextField(blank=True)
    noi_sent = models.CharField(max_length=20, blank=True)
    approved = models.DateTimeField(null=True, blank=True)
    received = models.DateField(null=True, blank=True)
    prior_permit = models.IntegerField(default=0)
    expiration_date = models.DateTimeField(null=True, blank=True)
    fire_prevention_districts = models.IntegerField(blank=True, null=True)
    police_districts = models.IntegerField(blank=True, null=True)
    supervisor_districts = models.IntegerField(blank=True, null=True)
    zip_codes = models.IntegerField(blank=True, null=True)
    neighborhoods = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['location_id']

    def __str__(self):
        return f'{self.applicant} - {self.location_id}'


class TruckFoodItem(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['truck', 'food_item'], name='truck_food_item_unique'),
        ]

