# Generated by Django 3.0.8 on 2020-10-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarios', '0012_reservas_deposito_inicial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservas',
            name='precio',
            field=models.IntegerField(default=0),
        ),
    ]
