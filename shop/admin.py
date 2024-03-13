from django.contrib import admin

from .models import *


class InlineProductImage(admin.TabularInline):
    model = ProductImage


class InlineOnlyView(admin.TabularInline):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class InlineAddress(InlineOnlyView):
    model = Address
    verbose_name_plural = model._meta.verbose_name


class InlineIndividual(InlineOnlyView):
    model = Individual
    verbose_name_plural = model._meta.verbose_name


class InlineOrderItem(InlineOnlyView):
    model = OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "season", "manufacturer", "visible"]
    list_filter = ["season", "visible"]
    search_fields = ["name"]
    inlines = [InlineProductImage]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ["id", "created", "total_price", "status"]
    readonly_fields = fields[:-1]
    list_filter = ["status"]
    inlines = [InlineAddress, InlineIndividual, InlineOrderItem]

    # def get_formsets_with_inlines(self, request, obj=None):
    #     """Динамически отображаем инлайны в зависимости от наличия связанной записи."""
    #     for inline in self.get_inline_instances(request, obj):
    #         # Пропускаем отображение инлайна, если нет связанных объектов
    #         if obj:  # Проверяем, что obj не None
    #             if inline.model == Individual and not Individual.objects.filter(order=obj).exists():
    #                 continue
    #             if inline.model == LegalEntity and not LegalEntity.objects.filter(order=obj).exists():
    #                 continue
    #         yield inline.get_formset(request, obj), inline
