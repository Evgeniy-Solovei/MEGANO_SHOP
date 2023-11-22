from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Product, Review
from catalog.serializers import CustomProductSerializer, ProductSerializer

from .cart import Cart


class CartView(APIView):
    """Представление для получения и удаления продуктов из корзины, добавления продуктов в корзину"""

    def get_cart_items(self, cart):
        cart_items = []
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            cart_items.append(
                {
                    "id": product.id,
                    "category": product.category.id,
                    "price": float(item["price"]),
                    "count": item["quantity"],
                    "date": product.data.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)"),
                    "title": product.title,
                    "description": product.description,
                    "freeDelivery": product.freeDelivery,
                    "images": [
                        {"src": product.image.src.url, "alt": product.image.alt}
                    ],
                    "tags": [
                        {"id": tag.id, "name": tag.name} for tag in product.tags.all()
                    ],
                    "reviews": Review.objects.filter(product=product).count(),
                    "rating": product.rating,
                }
            )
        return cart_items

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get("id")
        quantity = int(request.data.get("count", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.add(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def delete(self, request):
        product_id = request.data.get("id")
        quantity = request.data.get("count", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.remove(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)
