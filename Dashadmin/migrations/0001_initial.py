# Generated by Django 5.1.4 on 2025-03-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Add_mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('img_mission', models.ImageField(blank=True, null=True, upload_to='images_mission/')),
                ('lien', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Add_pubfb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_fb', models.CharField(max_length=100)),
                ('date_fb', models.DateTimeField(auto_now_add=True)),
                ('img_fb', models.ImageField(blank=True, null=True, upload_to='images_fb/')),
                ('lien_fb', models.URLField(blank=True, null=True)),
                ('description_fb', models.TextField()),
            ],
        ),
    ]
