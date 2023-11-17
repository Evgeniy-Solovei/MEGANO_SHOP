from django.urls import path
from order.views import OrdersView, OrderDetailsView

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order"),
]
