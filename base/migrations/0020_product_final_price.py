# Generated by Django 2.2.4 on 2019-11-09 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20191106_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
