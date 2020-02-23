# Generated by Django 2.2.4 on 2020-02-10 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_auto_20200209_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='iva_condition',
            field=models.CharField(choices=[('CTD', 'Contado'), ('RIN', 'Responsable Inscripto')], default='RIN', max_length=3),
        ),
    ]