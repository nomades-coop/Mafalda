# Generated by Django 2.2.4 on 2019-09-10 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20190910_1440'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presupuesto',
            old_name='discounts',
            new_name='discount',
        ),
    ]
