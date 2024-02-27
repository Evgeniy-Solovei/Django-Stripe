import os
import stripe
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from pay_stripe.product.models import Item


class BuyItemView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        """
        Функция создает сеанс оплаты Stripe для выбранного товара.

        Аргументы:
        - request: объект запроса Django
        - pk: первичный ключ товара, для которого создается сеанс оплаты.

        Возвращает:
        - JsonResponse с идентификатором сеанса оплаты (если успешно) или сообщением об ошибке (если возникает исключение).

        Использует:
        - get_object_or_404: функция Django, которая возвращает объект по первичному ключу или вызывает HTTP 404 Not Found,
          если объект не найден.
        - stripe.checkout.Session.create: метод Stripe API для создания сеанса оплаты.
        """
        item = get_object_or_404(Item, pk=pk)
        currency = request.GET.get('currency', 'usd')
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel'
            )
            return JsonResponse({'session_id': session.id})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': 'Произошла ошибка при создании сеанса оплаты'}, status=500)


class InfoItemView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Функция получает объект Item по его идентификатору и возвращает HTML страницу с этим объектом.

        Аргументы:
        - request: объект запроса Django
        - pk: идентификатор объекта Item

        Возвращает:
        - объект HttpResponse с HTML страницей, содержащей объект Item.
        """
        item = get_object_or_404(Item, pk=pk)
        context = {
            'item': item,
            'stripe_publishable_key': os.getenv('STRIPE_SECRET_KEY'),
        }
        return render(request, 'item.html', context=context)
