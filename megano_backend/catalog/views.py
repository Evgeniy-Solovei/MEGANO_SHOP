from django.db.models import Count, F
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import Profile

from .models import Category, Product, Review, Sale, Tag
from .pagination import CatalogPagination
from .serializers import (CategorySerializer, CustomProductSerializer,
                          ProductSerializer, ReviewSerializer, SaleSerializer,
                          TagSerializer)


class CategoryListView(ListAPIView):
    """Класс для отображения списка категорий и их подкатегорий"""

    queryset = Category.objects.filter(parent=None).prefetch_related("subcategories")
    serializer_class = CategorySerializer
    pagination_class = None


class TagListView(APIView):
    """Класс для отображения всех тегов"""

    def get(self, request: Request) -> Response:
        tags = Tag.objects.all()
        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data)


class CatalogListView(ListAPIView):
    """Класс для отображения всех товаров в интернет магазине"""

    serializer_class = ProductSerializer
    pagination_class = CatalogPagination

    def get_queryset(self) -> Response:
        queryset = Product.objects.all()
        if self.request.query_params:
            name = self.request.query_params.get("filter[name]")
            if name:
                queryset = queryset.filter(description__icontains=name)
            min_price = self.request.query_params.get("filter[minPrice]")
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            max_price = self.request.query_params.get("filter[maxPrice]")
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            free_delivery = self.request.query_params.get("filter[freeDelivery]")
            if free_delivery:
                queryset = queryset.filter(freeDelivery=True)
            available = self.request.query_params.get("filter[available]")
            if available:
                queryset = queryset.filter(available=True)
        order_by = self.request.query_params.get("sort")
        if order_by:
            if order_by == "rating":
                queryset = queryset.order_by("-rating")
            elif order_by == "price":
                # Сортировка по цене
                sort_type = self.request.query_params.get(
                    "sortType", "dec"
                )  # По умолчанию сортируем по убыванию
                if sort_type == "inc":
                    queryset = queryset.order_by("price")
                else:
                    queryset = queryset.order_by("-price")
            elif order_by == "reviews":
                # Сортировка по количеству отзывов
                queryset = queryset.annotate(num_reviews=Count("reviews")).order_by(
                    "-num_reviews"
                )
            elif order_by == "date":
                # Сортировка по дате
                sort_type = self.request.query_params.get(
                    "sortType", "dec"
                )  # По умолчанию сортируем по убыванию
                if sort_type == "inc":
                    queryset = queryset.order_by("data")
                else:
                    queryset = queryset.order_by("-data")

        return queryset


class ProductPopularListView(ListAPIView):
    """Модель для вывода популярных товаров"""

    queryset = Product.objects.annotate(count_reviews=Count("reviews")).order_by(
        "-count_reviews"
    )[:5]
    serializer_class = CustomProductSerializer
    pagination_class = None


class ProductLimitedListView(ListAPIView):
    """Модель для вывода лимитированных товаров"""

    queryset = Product.objects.all().order_by("-count")[:5]
    serializer_class = CustomProductSerializer
    pagination_class = None


class SaleProductList(ListAPIView):
    """Модель для вывода акционных товаров"""

    serializer_class = SaleSerializer
    pagination_class = CatalogPagination

    def get_queryset(self) -> Response:
        queryset = Sale.objects.filter(product__isnull=False).annotate(
            price=F("product__price"),
            title=F("product__title"),
            images=F("product__image"),
        )
        return queryset


class BannerProductList(ListAPIView):
    """Модель для вывода баннера на сайте"""

    queryset = Product.objects.all().order_by("?")[:5]
    serializer_class = ProductSerializer
    pagination_class = None


class ProductDetailsView(APIView):
    """Класс для отображения информации об экземпляре продукта"""

    def get(self, request: Request, pk: int) -> Response:
        product = Product.objects.get(pk=pk)
        serialized = CustomProductSerializer(product)
        return Response(serialized.data)


class ProductReviewsView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = Review.objects.filter(product__id=pk)
        return queryset

    def post(self, request: Request, pk: int) -> Response:
        try:
            product = Product.objects.get(pk=pk)
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
