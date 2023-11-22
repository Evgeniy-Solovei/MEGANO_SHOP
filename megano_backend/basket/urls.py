from django.urls import path

from basket.views import CartView

urlpatterns = [
    path("basket/", CartView.as_view(), name="basket"),
]
