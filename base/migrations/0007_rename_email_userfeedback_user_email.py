# Generated by Django 5.0.6 on 2024-07-02 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_userfeedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfeedback',
            old_name='email',
            new_name='user_email',
        ),
    ]
