# Generated by Django 5.0.6 on 2024-11-12 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_alter_notificationsettings_no_of_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='admin_response',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='response_sent',
            field=models.BooleanField(default=False),
        ),
    ]
