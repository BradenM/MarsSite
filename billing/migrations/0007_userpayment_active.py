# Generated by Django 2.0.5 on 2018-07-28 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_paymentcard_userpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]