# Generated by Django 3.2.15 on 2023-05-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0004_dish_stripe_price_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, upload_to='dishes_images'),
        ),
    ]
