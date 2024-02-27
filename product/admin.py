from django.contrib import admin
from product.models import Discount, Tax, Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Класс для управления товарами в административной панели.
    """
    list_display = ['name', 'description', 'price', 'currency']
    list_filter = ['name', 'price']
    ordering = ['name', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Класс для управления заказами в административной панели.
    """
    list_display = ['id', 'items', 'total_price', 'discount', 'tax']
    list_filter = ['id', 'total_price', 'discount', 'tax']
    ordering = ['id', ]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Класс для управления скидками в административной панели.
    """
    list_display = ['order', 'discount_value']
    ordering = ['order', ]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """
    Класс для управления налогом на заказ в административной панели.
    """
    list_display = ['order', 'tax_value']
    ordering = ['order', ]
