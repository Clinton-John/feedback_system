# Generated by Django 5.0.6 on 2024-07-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_alter_registeredorg_org_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredorg',
            name='org_qr_code',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]