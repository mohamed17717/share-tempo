# Generated by Django 4.1.7 on 2023-10-18 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteServe', '0006_alter_chatgptprompttemplate_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgptprompttemplate',
            name='template',
            field=models.TextField(verbose_name='Allowed labels are {product_name}, {product_description}, {product_seo_title}, or {keywords} || Keep in mind the DEPENDENCIES when choose the labels.'),
        ),
    ]
