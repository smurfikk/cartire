from django.contrib import admin

from .models import *


class InlineProductImage(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineProductImage]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
