# Generated by Django 2.0.5 on 2018-07-25 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_stripe', '0014_auto_20180413_1959'),
        ('store', '0010_auto_20180615_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='temp_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pinax_stripe.Card'),
        ),
    ]