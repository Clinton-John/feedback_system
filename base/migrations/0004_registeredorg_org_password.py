# Generated by Django 5.0.6 on 2024-06-28 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_created_by_registeredorg_org_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredorg',
            name='org_password',
            field=models.CharField(max_length=128, null=True),
        ),
    ]