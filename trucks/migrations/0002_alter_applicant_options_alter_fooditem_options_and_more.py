# Generated by Django 4.2.8 on 2023-12-07 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicant',
            options={'ordering': ['slug']},
        ),
        migrations.AlterModelOptions(
            name='fooditem',
            options={'ordering': ['slug']},
        ),
        migrations.AlterModelOptions(
            name='truck',
            options={'ordering': ['applicant_id']},
        ),
        migrations.RemoveField(
            model_name='truck',
            name='food_items',
        ),
        migrations.AddField(
            model_name='truck',
            name='food_items',
            field=models.ManyToManyField(blank=True, through='trucks.TruckFoodItem', to='trucks.fooditem'),
        ),
    ]
