# Generated by Django 4.2.7 on 2023-11-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vital_signs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vitalsigns",
            name="blood_pressure",
            field=models.CharField(max_length=10),
        ),
    ]
