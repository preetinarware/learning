# Generated by Django 3.2.7 on 2022-01-20 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_course_detail_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_detail',
            name='slug',
            field=models.SlugField(max_length=1000, null=True),
        ),
    ]
