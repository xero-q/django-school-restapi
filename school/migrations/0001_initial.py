# Generated by Django 5.1.1 on 2024-09-18 23:08

import school.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('dob', models.DateField(verbose_name='Birth Date')),
                ('sex', models.CharField(max_length=1, verbose_name='Sex')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Address')),
                ('phone', models.CharField(max_length=20, null=True, validators=[school.models.validate_phone_number], verbose_name='Phone number')),
            ],
        ),
    ]