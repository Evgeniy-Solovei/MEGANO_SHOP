from django.urls import path
from .views import CategoryListView, TagListView, ProductDetailsView, CatalogListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),




    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
]
