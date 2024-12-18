# Generated by Django 5.0.6 on 2024-06-28 23:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_registeredorg_org_password'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeredorg',
            name='org_admin',
        ),
        migrations.AddField(
            model_name='registeredorg',
            name='org_admins',
            field=models.ManyToManyField(related_name='admin_organizations', to=settings.AUTH_USER_MODEL),
        ),
    ]
