# Generated by Django 4.2.5 on 2024-04-01 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_transaction_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='total_coins',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='total_recycle',
            field=models.IntegerField(null=True),
        ),
    ]
