# Generated by Django 4.1.7 on 2023-05-05 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_sallawebhooklog'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChatGPTLog',
            new_name='ChatGPTResponse',
        ),
    ]
