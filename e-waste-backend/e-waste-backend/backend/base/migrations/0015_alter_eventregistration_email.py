# Generated by Django 5.0 on 2024-01-06 09:34

import base.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_eventregistration_email_eventregistration_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='email',
            field=base.models.LowercaseEmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
