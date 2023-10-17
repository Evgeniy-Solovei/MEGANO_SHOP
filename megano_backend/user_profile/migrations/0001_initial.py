# Generated by Django 4.2.5 on 2023-10-17 17:54

from django.db import migrations, models
import user_profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=50, verbose_name='Полное имя')),
                ('email', models.EmailField(max_length=100, verbose_name='Почта')),
                ('phone', models.IntegerField(blank=True, null=True, validators=[user_profile.models.validate_phone], verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=user_profile.models.avatar_image_directory_path, verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
