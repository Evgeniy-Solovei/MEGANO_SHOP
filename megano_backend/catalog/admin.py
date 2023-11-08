from django.contrib import admin

from .models import Category, Tag, Review, Specifications, Product, Sale, Image


class ImageAdmin(admin.ModelAdmin):
    list_display = 'src', 'alt'


admin.site.register(Image, ImageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'pk', 'title', 'parent', 'image'


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = 'name',


admin.site.register(Tag, TagAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = 'author', 'text', 'rate', 'data'


admin.site.register(Review, ReviewAdmin)


class SpecificationsAdmin(admin.ModelAdmin):
    list_display = 'name', 'value'


admin.site.register(Specifications, SpecificationsAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category',
                    'price',
                    'count',
                    'data',
                    'title',
                    'description',
                    'freeDelivery',
                    'image',
                    )


admin.site.register(Product, ProductAdmin)


class SaleAdmin(admin.ModelAdmin):
    list_display = 'product', 'salePrice', 'dateFrom', 'dateTo'


admin.site.register(Sale, SaleAdmin)
