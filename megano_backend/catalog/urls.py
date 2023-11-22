from django.urls import path

from .views import (BannerProductList, CatalogListView, CategoryListView,
                    ProductDetailsView, ProductLimitedListView,
                    ProductPopularListView, ProductReviewsView,
                    SaleProductList, TagListView)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("tags/", TagListView.as_view(), name="tags"),
    path("catalog/", CatalogListView.as_view(), name="catalog"),
    path(
        "products/popular/", ProductPopularListView.as_view(), name="products_popular"
    ),
    path(
        "products/limited/", ProductLimitedListView.as_view(), name="products_limited"
    ),
    path("sales/", SaleProductList.as_view(), name="sale"),
    path("banners/", BannerProductList.as_view(), name="banner"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path(
        "product/<int:pk>/reviews/",
        ProductReviewsView.as_view(),
        name="product_reviews",
    ),
]
