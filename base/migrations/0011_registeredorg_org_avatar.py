# Generated by Django 5.0.6 on 2024-07-10 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredorg',
            name='org_avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]