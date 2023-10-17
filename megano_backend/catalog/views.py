# from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Category, Tag, Product
from .serializers import ProductSerialized


class CategoryListView(APIView):
    """Класс для отображения списка категорий и их подкатегорий в формате Json"""

    def get(self, request: Request) -> JsonResponse:
        categories = Category.objects.filter(subcategories=None)
        categories_data = []
        for category in categories:
            subcategories_data = []
            subcategories = Category.objects.filter(subcategories=category)
            if subcategories:
                for subcategory in subcategories:
                    sub_data = {
                        'id': subcategory.pk,
                        'title': subcategory.title,
                        'image': subcategory.get_image(),
                    }
                    subcategories_data.append(sub_data)
            data_cat = {
                'id': category.pk,
                'title': category.title,
                'image': category.get_image(),
                'subcategories': subcategories_data,
            }
            categories_data.append(data_cat)
        return JsonResponse(categories_data, safe=False)
        # return Response({'categories_data': categories_data})


class TagListView(APIView):
    """Класс для отображения всех тегов в Json-формате"""

    def get(self, request: Request) -> JsonResponse:
        tags = Tag.objects.all()
        tags_list = []
        for tag in tags:
            data_tag = {
                'id': tag.id,
                'name': tag.name,
            }
            tags_list.append(data_tag)
        return JsonResponse(tags_list, safe=False)
        # return Response({'tags_list': tags_list})


class CatalogListView(APIView):
    """Класс для отображения всех товаров в интернет магазине"""

    def get(self, request: Request) -> JsonResponse:
        products = Product.objects.all()
        serialized = ProductSerialized(products, many=True)
        return JsonResponse({"items": serialized.data})


class ProductDetailsView(APIView):
    """Класс для отображения информации об экземпляре продукта в Json-формате ЧЕРНОВИК"""
    def get(self, request: Request) -> JsonResponse:
        ...
#         products = Product.objects.all().values()
#         return JsonResponse({'items': list(products)})
