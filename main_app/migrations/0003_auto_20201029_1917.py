# Generated by Django 3.0.5 on 2020-10-29 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20201029_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(decimal_places=50, max_digits=60),
        ),
        migrations.AlterField(
            model_name='location',
            name='long',
            field=models.DecimalField(decimal_places=50, max_digits=60),
        ),
    ]
