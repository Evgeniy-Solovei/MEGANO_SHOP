from rest_framework.request import Request
from rest_framework.response import Response

from catalog.models import Product, Tag, Category, Review, Sale
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.fullName', read_only=True)
    email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Review
        fields = 'author', 'email', 'text', 'rate', 'date'


class SaleSerializer(serializers.ModelSerializer):
    id = serializers.ImageField(source='sales.id', read_only=True)
    price = serializers.DecimalField(source='sales.price', decimal_places=2, max_digits=8, read_only=True)
    title = serializers.CharField(source='sales.title', read_only=True)
    images = serializers.ImageField(source='sales.image.images', read_only=True)

    class Meta:
        model = Sale
        fields = 'id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images'
