# Generated by Django 2.0.5 on 2018-06-15 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20180612_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercart',
            name='total',
            field=models.FloatField(default='0.00'),
        ),
    ]
