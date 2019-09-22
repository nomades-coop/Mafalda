# Generated by Django 2.2.4 on 2019-09-10 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20190910_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='presupuesto_total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='product_total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
