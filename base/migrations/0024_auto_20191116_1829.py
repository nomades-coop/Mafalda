# Generated by Django 2.2.4 on 2019-11-16 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_presupuesto_company_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presupuesto',
            old_name='company_id',
            new_name='company',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='company_id',
            new_name='company',
        ),
    ]
