# Generated by Django 4.2.1 on 2023-05-25 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0005_alter_dish_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]