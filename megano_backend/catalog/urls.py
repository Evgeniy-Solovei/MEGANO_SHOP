from django.urls import path
from .views import (
    CategoryListView,
    TagListView,
    ProductDetailsView,
    CatalogListView,
    ProductLimitedListView,
    ProductPopularListView,
    BannerProductList,
    SaleProductList,

)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('products/popular/', ProductPopularListView.as_view(), name='products_popular'),
    path('products/limited/', ProductLimitedListView.as_view(), name='products_limited'),
    path('sales/', SaleProductList.as_view(), name='sale'),
    path('banners/', BannerProductList.as_view(), name='banner'),
    path('product/<int:pk>/review/', ProductDetailsView.as_view(), name='product_reviews'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
]
