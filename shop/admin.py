from django.contrib import admin

from .models import *


class InlineProductImage(admin.TabularInline):
    model = ProductImage


class InlineAddress(admin.TabularInline):
    model = Address


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineProductImage]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
    # inlines = [InlineAddress]
