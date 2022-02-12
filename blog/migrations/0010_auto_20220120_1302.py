# Generated by Django 3.2.7 on 2022-01-20 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_instructor_slug'),
        ('blog', '0009_blog_detail_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_detail',
            name='blog_img',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='blog_detail',
            name='blog_instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_detail', to='user_profile.instructor'),
        ),
        migrations.AlterField(
            model_name='blog_detail',
            name='head1',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blog_detail',
            name='head2',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blog_detail',
            name='setting',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blog_detail',
            name='slug',
            field=models.SlugField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='blog_detail',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='blog_detail',
            name='why_need',
            field=models.TextField(),
        ),
    ]
