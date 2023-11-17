# Generated by Django 4.2.5 on 2023-11-15 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0003_alter_profile_options'),
        ('catalog', '0006_remove_product_review_remove_product_specification_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время заказа')),
                ('deliveryType', models.CharField(choices=[('regular', 'Обычная доставка'), ('express', 'Экспресс доставка')], default='regular', max_length=50, verbose_name='Тип доставки')),
                ('paymentType', models.CharField(choices=[('online', 'Онлайн картой'), ('online_2', 'Онлайн со случайного чужого счета')], default='online', max_length=100, verbose_name='Тип оплаты')),
                ('status', models.CharField(choices=[('Created', 'Создан'), ('Paid', 'Оплачен'), ('Sent', 'Отправлен'), ('Arrived', 'Пришел')], default='Created', max_length=100, verbose_name='Статус заказа')),
                ('city', models.CharField(default='', max_length=100, verbose_name='Город')),
                ('address', models.CharField(default='', max_length=255, verbose_name='Адрес доставки')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.profile', verbose_name='Профиль пользователя')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество товаров в заказе')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_in_order', to='order.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Продукт')),
            ],
        ),
    ]
