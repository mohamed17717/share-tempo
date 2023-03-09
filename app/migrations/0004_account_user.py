# Generated by Django 4.1.7 on 2023-03-09 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_account_refresh_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]