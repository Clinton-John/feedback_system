# Generated by Django 5.0.6 on 2024-08-13 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_remove_orgprofile_org_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='submited_to',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]