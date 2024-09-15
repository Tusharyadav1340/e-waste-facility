# Generated by Django 4.2.5 on 2024-04-02 05:30

import base.register.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_facility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='email',
            field=base.register.models.LowercaseEmailField(max_length=254, null=True, verbose_name='email address'),
        ),
    ]
