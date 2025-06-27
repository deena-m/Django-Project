# flipkartapp/admin.py
from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Product

class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
