# Generated by Django 3.2.7 on 2022-01-17 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0004_auto_20220115_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='blog_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_category', models.CharField(max_length=100)),
                ('blog_title', models.CharField(max_length=500)),
                ('blog_img', models.ImageField(blank=True, upload_to='')),
                ('blog_description', models.TextField()),
                ('blog_created_date', models.DateField(auto_now=True)),
                ('tags', models.CharField(max_length=100, null=True)),
                ('head1', models.TextField(null=True)),
                ('head2', models.TextField(null=True)),
                ('head3', models.TextField(null=True)),
                ('head4', models.TextField(null=True)),
                ('blog_instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_detail', to='user_profile.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='blogdetail_img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgs', models.ImageField(upload_to='')),
                ('blogs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog_detail')),
            ],
        ),
        migrations.CreateModel(
            name='blogdetail_element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgs', models.CharField(max_length=100)),
                ('blogs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog_detail')),
            ],
        ),
    ]
