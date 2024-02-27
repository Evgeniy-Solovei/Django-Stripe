from django.db import models


class Item(models.Model):
    """
    Модель товара в магазине.

        Атрибуты:
        name (CharField): Название товара.
        description (TextField): Описание товара.
        price (DecimalField): Цена товара.
    """

    name = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Модель заказа в магазине

        Атрибуты:
        items (ManyToManyField): Товары в заказе.
        total_price (DecimalField): Цена заказа.
        discount (ForeignKey) : Скидка на заказ.
        tax (ForeignKey) : Налог на заказ.
    """
    items = models.ManyToManyField(Item, related_name='item_all_orders', verbose_name='Товары')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа')
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Скидка')
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Налог')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Сумма заказа: {self.total_price}'


class Discount(models.Model):
    """
    Модель скидки

        Атрибуты:
        order (ForeignKey): Заказы со скидкой.
        discount_value (DecimalField): Размер скидки в %.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_all_discounts', verbose_name='Заказы')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Скидка в %')

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f'Ваша скидка: {self.discount_value} %'


class Tax(models.Model):
    """
    Модель налога

        Атрибуты:
        order (ForeignKey): Заказы с налогом.
        discount_value (DecimalField): Размер налога в %.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказы')
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Налог в %')

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return f'Ваш налог: {self.tax_value} %'
