from django.urls import path

from order.views import OrderDetailsView, OrdersView, PaymentOrderView

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order"),
    path("payment/<int:pk>/", PaymentOrderView.as_view(), name="order"),
]
