from django.db import models
from catalog.models import Product
from user_profile.models import Profile


class Order(models.Model):
    """Модель заказ, для покупки товара"""

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время заказа')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Профиль пользователя")

    DELIVERY_CHOICES = ('regular', 'Обычная доставка'), ('express', 'Экспресс доставка')
    deliveryType = models.CharField(max_length=50, choices=DELIVERY_CHOICES, default='regular',
                                    verbose_name="Тип доставки")

    PAYMENT_CHOICES = ('online', 'Онлайн картой'), ('online_2', 'Онлайн со случайного чужого счета')
    paymentType = models.CharField(max_length=100, choices=PAYMENT_CHOICES, default='online', verbose_name="Тип оплаты")

    STATUS_CHOICES = ('Created', 'Создан'), ('Paid', 'Оплачен'), ('Sent', 'Отправлен'), ('Arrived', 'Пришел')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Created', verbose_name="Статус заказа")

    city = models.CharField(max_length=100, default='', verbose_name="Город")
    address = models.CharField(max_length=255, default='', verbose_name="Адрес доставки")

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    """Модель продуктов в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name='products_in_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество товаров в заказе')

    def __str__(self):
        return str(self.id)
