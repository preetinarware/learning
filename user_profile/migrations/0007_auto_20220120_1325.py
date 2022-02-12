# Generated by Django 3.2.7 on 2022-01-20 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0006_instructor_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='expert',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='slug',
            field=models.SlugField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='auth.user'),
        ),
    ]
