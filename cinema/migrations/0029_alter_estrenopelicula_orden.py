# Generated by Django 5.1.6 on 2025-03-11 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0028_contenidocine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estrenopelicula',
            name='orden',
            field=models.IntegerField(default=0),
        ),
    ]
