# Generated by Django 5.0.6 on 2024-06-27 20:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredOrg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=100, null=True)),
                ('org_email', models.EmailField(max_length=100, null=True)),
                ('org_descr', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('org_admins', models.ManyToManyField(related_name='adminstered_org', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
