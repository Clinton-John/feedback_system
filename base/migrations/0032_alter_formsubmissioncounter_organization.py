# Generated by Django 5.0.6 on 2024-10-01 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_formsubmissioncounter_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsubmissioncounter',
            name='organization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='submission_counter', to='base.registeredorg'),
        ),
    ]