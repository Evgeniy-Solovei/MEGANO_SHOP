# Generated by Django 4.2.5 on 2023-10-26 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_sale'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specifications',
            options={'verbose_name': 'Характеристика товара', 'verbose_name_plural': 'Характеристики товаров'},
        ),
    ]