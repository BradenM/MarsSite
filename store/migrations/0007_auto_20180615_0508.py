# Generated by Django 2.0.5 on 2018-06-15 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_cartentry_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartentry',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='repair.DeviceRepair'),
        ),
    ]