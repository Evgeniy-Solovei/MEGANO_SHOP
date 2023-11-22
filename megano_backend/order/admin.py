from django.contrib import admin

from order.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "createdAt",
        "profile",
        "deliveryType",
        "paymentType",
        "status",
        "city",
        "address",
    )


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")


admin.site.register(OrderItem, OrderItemAdmin)
