from rest_framework import serializers

from catalog.models import Product
from catalog.serializers import ProductSerializer
from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ("id", "order", "product", "price", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, source="products_in_order")
    fullName = serializers.CharField(source="profile.fullName", read_only=True)
    email = serializers.CharField(source="profile.email", read_only=True)
    phone = serializers.CharField(source="profile.phone", read_only=True)
    totalCost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        )

    def get_totalCost(self, obj):
        order_items = obj.products_in_order.all()
        total_cost = sum(float(item.price) * item.quantity for item in order_items)
        return total_cost
