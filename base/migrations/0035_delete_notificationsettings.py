# Generated by Django 5.0.6 on 2024-10-07 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_alter_notificationsettings_no_of_notifications_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NotificationSettings',
        ),
    ]
