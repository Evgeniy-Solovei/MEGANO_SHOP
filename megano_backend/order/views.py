from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.cart import Cart
from catalog.models import Product
from order.models import Order, OrderItem
from order.serializers import OrderSerializer


class OrdersView(APIView):
    """Класс Заказы: для просмотра заказов (get), добавление заказа (post)"""

    def get(self, request: Request) -> Response:
        orders = Order.objects.filter(profile=request.user.profile).order_by(
            "-createdAt"
        )
        serialized = OrderSerializer(orders, many=True)
        return Response(serialized)

    def post(self, request: Request) -> Response:
        cart = Cart(request)
        order = Order.objects.create(profile=request.user.profile)
        order_items = [
            OrderItem(
                order=order,
                product=item["product_id"],
                price=item["price"],
                quantity=item["quantity"],
            )
            for item in cart
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.clear()
        return Response({" orderId": order.pk}, status=200)


class OrderDetailsView(APIView):
    """Класс для просмотра деталей заказа (get) и его редактирование (post)"""

    def get(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        serialized = OrderSerializer(order)
        return Response(serialized.data)

    def post(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        order.profile.firstName = request.data["profile"]["firstName"]
        order.profile.email = request.data["profile"]["email"]
        order.profile.phone = request.data["profile"]["phone"]
        order.deliveryType = request.data["deliveryType"]
        order.paymentType = request.data["paymentType"]
        order.status = request.data["status"]
        order.city = request.data["city"]
        order.address = request.data["address"]
        order.save()
        serialized = OrderSerializer(order, many=True)
        return Response(serialized.data)


class PaymentOrderView(APIView):
    """Класс оплаты заказа"""

    def post(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        number = request.data.get("number")
        name = request.data.get("name")
        month = request.data.get("month")
        year = request.data.get("year")
        code = request.data.get("code")
        if order.paymentType == "online":
            if number.isdigit() and len(number) <= 8:
                if int(number) % 2 == 0 and int(number[-1]) != 0:
                    return Response(
                        {
                            "number": number,
                            "name": name,
                            "month": month,
                            "year": year,
                            "code": code,
                        },
                        status=200,
                    )
                else:
                    return Response(status=400)
            else:
                return Response(status=400)
        else:
            if number.isdigit() and len(number) <= 8:
                if int(number) % 2 == 0 and int(number[-1]) != 0:
                    return Response(
                        {
                            "number": number,
                            "name": name,
                            "month": month,
                            "year": year,
                            "code": code,
                        },
                        status=200,
                    )
                else:
                    return Response(status=400)
            else:
                return Response(status=400)
