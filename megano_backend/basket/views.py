from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models import Product
from catalog.serializers import ProductSerializer, CustomProductSerializer
from .cart import Cart


def get_products_in_cart(cart):
    """Получение продуктов из корзины и их сериализация."""

    products_in_cart = [product for product in cart.cart.keys()]
    products = Product.objects.filter(pk__in=products_in_cart)
    serializer = CustomProductSerializer(products, many=True, context=cart.cart)
    return serializer


class CartView(APIView):
    """Представление для получения и удаления продуктов из корзины, добавления продуктов в корзину"""

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)

    def post(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.request.data.get('id'))
        cart.add(product=product, quantity=self.request.data.get('quantity'))
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)

    def delete(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.request.data.get('id'))
        count = self.request.data.get('quantity', False)
        cart.remove(product, count=count)
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)
