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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(source='image')
    tags = TagSerializer(many=True)
    # date = serializers.DateTimeField(format="%a %b %d %Y %H:%M:%S GMT%z (Central European Standard Time)", source='data')
    date = serializers.DateTimeField(source='data')
    reviews = serializers.PrimaryKeyRelatedField(source='review', read_only=True)
    rating = serializers.SerializerMethodField()
    # price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'freeDelivery', 'images', 'tags',
                  'reviews', 'rating')

    def get_rating(self, obj):
        return obj.rating





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
