# Generated by Django 5.0.7 on 2024-08-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_rename_massage_people_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='phone_number',
            field=models.IntegerField(max_length=11, verbose_name='телефон'),
        ),
    ]