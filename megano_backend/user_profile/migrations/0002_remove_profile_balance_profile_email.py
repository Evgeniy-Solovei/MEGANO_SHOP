# Generated by Django 4.2.5 on 2023-10-25 21:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="balance",
        ),
        migrations.AddField(
            model_name="profile",
            name="email",
            field=models.EmailField(
                default="null", max_length=255, unique=True, verbose_name="Почта"
            ),
            preserve_default=False,
        ),
    ]
