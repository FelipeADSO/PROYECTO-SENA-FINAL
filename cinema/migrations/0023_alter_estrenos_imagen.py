# Generated by Django 5.1.6 on 2025-03-08 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0022_estrenos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estrenos',
            name='imagen',
            field=models.ImageField(upload_to='estrenos/'),
        ),
    ]
