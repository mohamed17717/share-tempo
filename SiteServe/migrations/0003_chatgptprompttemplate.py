# Generated by Django 4.1.7 on 2023-04-13 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteServe', '0002_alter_staticpage_options_staticpage_nav_ordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGPTPromptTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.TextField(verbose_name='Allowed labels are {product_name}, {product_description}, {product_seo_title}, or {keywords} || Keep in mind the DEPENDENCIES when choose the labels.')),
                ('type', models.CharField(choices=[('description', 'description'), ('seo_title', 'seo_title')], max_length=200)),
                ('language', models.CharField(choices=[('ar', 'ar'), ('en', 'en')], max_length=2)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]