# Generated by Django 3.2.7 on 2022-01-18 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20220114_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_detail',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='course_detail',
            name='course_certificate',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='course_detail',
            name='course_duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='course_detail',
            name='course_quiz',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
