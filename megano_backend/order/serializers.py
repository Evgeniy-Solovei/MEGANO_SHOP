from rest_framework import serializers

from catalog.serializers import ProductSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    fullName = serializers.CharField(source='profile.fullName', read_only=True)
    email = serializers.CharField(source='profile.email', read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    totalCost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'totalCost',
                  'status', 'city', 'address', 'products')

    def get_totalCost(self, obj):
        order_items = obj.products_in_order.all()
        total_cost = sum(item.price * item.quantity for item in order_items)
        return total_cost
