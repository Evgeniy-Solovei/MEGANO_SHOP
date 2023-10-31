from django.db.models import Count, F
from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Category, Tag, Product, Sale
from .pagination import CatalogPagination
from .serializers import ProductSerializer, TagSerializer, CategorySerializer, ReviewSerializer, SaleSerializer, \
    CustomProductSerializer


# class CategoryListView(APIView):
#     """Класс для отображения списка категорий и их подкатегорий"""
#
#     def get(self, request: Request) -> JsonResponse:
#         categories = Category.objects.filter(parent=None).prefetch_related("subcategories")
#         serialized = CategorySerializer(categories, many=True)
#         return JsonResponse(serialized.data)


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
        return queryset


class ProductPopularListView(ListAPIView):
    """Модель для вывода популярных товаров"""
    queryset = Product.objects.annotate(count_reviews=Count('review')).order_by('-count_reviews')[:5]
    serializer_class = CustomProductSerializer
    pagination_class = None


class ProductLimitedListView(ListAPIView):
    """Модель для вывода лимитированных товаров"""
    queryset = Product.objects.all().order_by('-count')[:5]
    serializer_class = CustomProductSerializer
    pagination_class = None


class SaleProductList(ListAPIView):
    """Модель для вывода акционных товаров"""
    serializer_class = SaleSerializer
    pagination_class = CatalogPagination

    def get_queryset(self) -> Response:
        queryset = Sale.objects.filter(product__isnull=False)
        return queryset


class BannerProductList(ListAPIView):
    """Модель для вывода баннера на сайте"""
    queryset = Product.objects.all().order_by('?')[:5]
    serializer_class = ProductSerializer
    pagination_class = None


class ProductDetailsView(APIView):
    """Класс для отображения информации об экземпляре продукта"""
    # serializer_class = ReviewSerializer
    # pagination_class = None

    def get(self, request: Request, pk: int) -> Response:
        product = Product.objects.get(pk=pk)
        serialized = ProductSerializer(product)
        return Response(serialized.data)

    def post(self, request: Request, pk: int) -> Response:
        data = request.data
        data['author'] = request.GET.get(request.user)
        data['text'] = request.GET.get('text')
        serialized = ReviewSerializer(data=data)
        if serialized.is_valid():
            review = serialized.save(author=pk)
            return Response(serialized.data)
        else:
            return Response(serialized.errors)
