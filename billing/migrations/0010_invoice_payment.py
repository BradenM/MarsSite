# Generated by Django 2.0.5 on 2018-07-28 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0009_auto_20180728_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='billing.UserPayment'),
        ),
    ]