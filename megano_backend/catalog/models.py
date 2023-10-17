
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from user_profile.models import Profile


def category_image_directory_path(instance: 'Category', filename: str) -> str:
    return f"categories/category_{instance.pk}/image/{filename}"


def product_image_directory_path(instance: 'Product', filename: str) -> str:
    return f"products/product_{instance.pk}/image/{filename}"


class Category(models.Model):
    """Модель Category представляет категории товаров, которые есть в интернет магазине."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title', ]

    title = models.CharField(max_length=100, verbose_name='Категория')
    subcategories = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Категория является подкатегорией от'
    )
    image = models.ImageField(null=True, blank=True, upload_to=category_image_directory_path,
                              verbose_name='Изображение')

    def __str__(self):
        return self.title

    def get_image(self):
        return {'src': self.image.url, 'alt': self.image.name}


class Tag(models.Model):
    """Модель Tag представляет создание тегов для товаров"""

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Review предоставляет возможность создавать отзывы о товаров"""

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Имя пользователя'
    )
    text = models.TextField(verbose_name='Отзыв')
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=0, verbose_name='Рейтинг'
    )
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text.verbose_name


class Specifications(models.Model):
    """Модель Specifications представляет характеристику товара"""

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=100, verbose_name='Имя характеристики')
    value = models.CharField(max_length=200, verbose_name='Значение характеристики')

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель Product представляет товар, который можно продавать в интернет-магазине."""

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Цена')
    count = models.PositiveIntegerField(verbose_name='Количество продукта в наличии')
    data = models.DateTimeField(verbose_name='Дата и время')
    title = models.CharField(max_length=100, verbose_name='Каталог')
    description = models.CharField(max_length=100, verbose_name='Описание')
    freeDelivery = models.BooleanField(default=True, verbose_name='Бесплатная доставка')
    images = models.ImageField(
        blank=True, null=True, upload_to=product_image_directory_path, verbose_name='Изображение'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тег')
    reviews = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Отзывы')
    specifications = models.ForeignKey(
        Specifications, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Характеристики продукта'
    )
    # rating = models.DecimalField(default=0, max_digits=8, decimal_places=1, verbose_name='Рейтинг')
    @property
    def rating(self) -> float:
        """Функция для вычисления среднего рейтинга с использованием .aggregate()"""
        reviews = Review.objects.filter(product=self)
        average_rating = reviews.aggregate(average_rating=Avg('rate'))['average_rating']

        if average_rating is not None:
            return round(average_rating, 2)
        else:
            return 0.0

    def __str__(self):
        return self.title

