# Generated by Django 2.0.5 on 2018-06-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair', '0005_auto_20180612_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicerepair',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
