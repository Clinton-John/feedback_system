# Generated by Django 5.0.6 on 2024-10-08 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0040_notificationsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationsettings',
            name='no_of_notifications',
            field=models.IntegerField(default=1),
        ),
    ]
