from django.db.models import Count, F
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Category, Tag, Product, Sale
from .pagination import CatalogPagination
from .serializers import ProductSerializer, TagSerializer, CategorySerializer, ReviewSerializer, SaleSerializer
import json

# class CategoryListView(APIView):
#     """Класс для отображения списка категорий и их подкатегорий"""
#
#     def get(self, request: Request) -> JsonResponse:
#         categories = Category.objects.filter(parent=None).prefetch_related("subcategories")
#         serialized = CategorySerializer(categories, many=True)
#         return JsonResponse(serialized.data)
def banners(request):
	data = [
		{
			"id": "123",
			"category": 55,
			"price": 500.67,
			"count": 12,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
				{
					"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
					"alt": "any alt text",
				}
			],
			"tags": [
				"string"
			],
			"reviews": 5,
			"rating": 4.6
		},
	]
	return JsonResponse(data, safe=False)


def basket(request):
	if(request.method == "GET"):
		print('[GET] /api/basket/')
		data = [
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
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			},
			{
				"id": 124,
				"category": 55,
				"price": 201.675,
				"count": 5,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

	elif (request.method == "POST"):
		body = json.loads(request.body)
		id = body['id']
		count = body['count']
		print('[POST] /api/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))
		data = [
			{
				"id": id,
				"category": 55,
				"price": 500.67,
				"count": 13,
				"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
				"title": "video card",
				"description": "description of the product",
				"freeDelivery": True,
				"images": [
						{
							"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
							"alt": "hello alt",
						}
				 ],
				 "tags": [
						{
							"id": 0,
							"name": "Hello world"
						}
				 ],
				"reviews": 5,
				"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)

	elif (request.method == "DELETE"):
		body = json.loads(request.body)
		id = body['id']
		print('[DELETE] /api/basket/')
		data = [
			{
			"id": id,
			"category": 55,
			"price": 500.67,
			"count": 11,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
						"alt": "hello alt",
					}
			 ],
			 "tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
			 ],
			"reviews": 5,
			"rating": 4.6
			}
		]
		return JsonResponse(data, safe=False)


def productsPopular(request):
	data = [
		{
			"id": "123",
			"category": 55,
			"price": 500.67,
			"count": 12,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
						"alt": "hello alt",
					}
			 ],
			 "tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
			 ],
			"reviews": 5,
			"rating": 4.6
		}
	]
	return JsonResponse(data, safe=False)

def productsLimited(request):
	data = [
		{
			"id": "123",
			"category": 55,
			"price": 500.67,
			"count": 12,
			"date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
			"title": "video card",
			"description": "description of the product",
			"freeDelivery": True,
			"images": [
					{
						"src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
						"alt": "hello alt",
					}
			 ],
			 "tags": [
					{
						"id": 0,
						"name": "Hello world"
					}
			 ],
			"reviews": 5,
			"rating": 4.6
		}
	]
	return JsonResponse(data, safe=False)


class CategoryListView(ListAPIView):
    """Класс для отображения списка категорий и их подкатегорий"""
    queryset = Category.objects.filter(parent=None).prefetch_related("subcategories")
    serializer_class = CategorySerializer
    pagination_class = None
    # print(serializer_class.data)


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
    serializer_class = ProductSerializer


class ProductLimitedListView(ListAPIView):
    """Модель для вывода лимитированных товаров"""
    queryset = Product.objects.all().order_by('-count')[:5]
    serializer_class = ProductSerializer


class SaleProductList(ListAPIView):
    """Модель для вывода акционных товаров"""
    serializer_class = SaleSerializer
    pagination_class = CatalogPagination

    def get_queryset(self) -> Response:
        queryset = Sale.objects.filter(sales__is_null=False).annotate(
            id=F('sales__id'),
            price=F('sales_price'),
            title=F('sales_title'),
            images=F('sales_image'),
        )
        return Response(queryset)


class BannerProductList(ListAPIView):
    """Модель для вывода баннера на сайте"""
    queryset = Product.objects.all().order_by('?')[:5]
    serializer_class = ProductSerializer


class ProductDetailsView(APIView):
    """Класс для отображения информации об экземпляре продукта"""

    def get(self, request: Request) -> Response:
        product = Product.objects.get(pk=self.pk)
        serialized = ProductSerializer(product)
        return Response(serialized.data)

    def post(self, review, request: Request) -> Response:
        product_reviews = Product.objects.get(pk=self.pk).prefetch_related("reviews")
        serialized = ReviewSerializer(product_reviews)
        return Response(serialized.data)
