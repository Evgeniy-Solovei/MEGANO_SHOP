from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'pk', 'title', 'subcategories', 'image'


admin.site.register(Category, CategoryAdmin)
