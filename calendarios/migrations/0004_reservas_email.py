# Generated by Django 3.0.2 on 2020-01-13 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarios', '0003_auto_20200109_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservas',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
