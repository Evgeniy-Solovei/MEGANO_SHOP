from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from basket.cart import Cart
from catalog.models import Product
from order.models import Order, OrderItem
from order.serializers import OrderSerializer


class OrdersView(APIView):
    """Класс Заказы: для просмотра заказов (get), добавление заказа (post)"""

    def get(self, request: Request) -> Response:
        order = Order.objects.all()
        serialized = OrderSerializer(order, many=True)
        return Response(serialized.data)

    # def post(self, request, *args, **kwargs):
    #     cart = Cart(request)
    #
    #     data = {
    #         'deliveryType': request.data.get('deliveryType'),
    #         'paymentType': request.data.get('paymentType'),
    #         'status': request.data.get('status'),
    #         'city': request.data.get('city'),
    #         'address': request.data.get('address'),
    #         # Добавьте другие поля заказа, если необходимо
    #     }
    #
    #     serializer = OrderSerializer(data=data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         cart.clear()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        # Проверка, является ли request.data списком
        if isinstance(request.data, list):
            data = request.data[0]  # Возьмите первый элемент из списка
        else:
            data = request.data

        serializer = OrderSerializer(data={
            "products": [
                {
                    "id": 123,
                    "category": 55,
                    "price": 500.67,
                    "count": 12,
                    "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                    "title": "video card",
                    "description": "description of the product",
                    "freeDelivery": True,
                    "images": [
                        {
                            "src": "/3.png",
                            "alt": "Image alt string"
                        }
                    ],
                    "tags": [
                        {
                            "id": 12,
                            "name": "Gaming"
                        }
                    ],
                    "reviews": 5,
                    "rating": 4.6
                }
            ]
        })

        if serializer.is_valid():
            serializer.save()
            cart.clear()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request: Request) -> Response:
    #     cart = Cart(request)
    #     for a in cart:
    #         Order.objects.create(
    #                                  createdAt=a.createdAt,
    #                                  profile=request.data.get('profile'),
    #                                  deliveryType=request.data.get('deliveryType'),
    #                                  paymentType=request.data.get('paymentType'),
    #                                  status=request.data.get('status'),
    #                                  address=request.data.get('address'))
    #     for product in cart:
    #         OrderItem.objects.create(order=request.order,
    #                                  product=product.product,
    #                                  price=product.price,
    #                                  quantity=product.quantity)
    #     cart.clear()
    #     serialized = OrderSerializer(a)
    #     return Response(serialized.data)


class OrderDetailsView(APIView):
    """Класс для просмотра деталей заказа (get) и его редактирование (post)"""

    def get(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        serialized = OrderSerializer(order)
        return Response(serialized.data)

    ...
