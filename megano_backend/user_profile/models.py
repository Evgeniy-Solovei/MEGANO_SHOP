from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


def validate_phone(value=375298945462):
    if len(str(value)) < 7:
        raise ValidationError("Номер телефона должен содержать более 7 цифры.")


def avatar_image_directory_path(instance: 'Profile', filename: str) -> str:
    return f"profiles/profile_{instance.pk}/image/{filename}"


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    fullName = models.CharField(max_length=50, verbose_name='Полное имя')
    email = models.EmailField(max_length=100, verbose_name='Почта')
    phone = models.IntegerField(validators=[validate_phone], blank=True, null=True, verbose_name='Номер телефона')
    avatar = models.ImageField(
        null=True, blank=True, upload_to=avatar_image_directory_path, verbose_name='Изображение'
    )

