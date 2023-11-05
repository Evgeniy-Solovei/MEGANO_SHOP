from rest_framework.request import Request
from rest_framework.response import Response

from catalog.models import Product, Tag, Category, Review, Sale, Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('src', 'alt')

    def to_representation(self, instance):
        return [{
            'src': instance.src.url,
            'alt': instance.alt
        }]


class ImageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('src', 'alt')

    def to_representation(self, instance):
        return {
            'src': instance.src.url,
            'alt': instance.alt
        }


class SubcategorySerializer(serializers.ModelSerializer):
    image = ImageCategorySerializer()

    class Meta:
        model = Category
        fields = 'id', 'title', 'image'


class CategorySerializer(serializers.ModelSerializer):
    image = ImageCategorySerializer()
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = 'id', 'title', 'image', 'subcategories'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.fullName', read_only=True)
    email = serializers.EmailField(source='author.email', read_only=True)
    date = serializers.DateTimeField(source='data')

    class Meta:
        model = Review
        fields = 'author', 'email', 'text', 'rate', 'date'


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(source='image')
    tags = TagSerializer(many=True)
    date = serializers.DateTimeField(source='data')
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'freeDelivery', 'images', 'tags',
                  'reviews', 'rating', 'available')

    def get_rating(self, obj):
        return obj.rating


class CustomProductSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'freeDelivery', 'images', 'tags',
                  'reviews', 'rating')


class SaleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.pk', read_only=True)
    price = serializers.DecimalField(source='product.price', decimal_places=2, max_digits=8, read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    images = ImageSerializer(source='product.image', read_only=True)

    class Meta:
        model = Sale
        fields = 'id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images'
