# Generated by Django 3.2.7 on 2022-01-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20220120_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
