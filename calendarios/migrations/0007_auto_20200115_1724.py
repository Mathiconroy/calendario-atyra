# Generated by Django 3.0.2 on 2020-01-15 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarios', '0006_auto_20200115_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservas',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
