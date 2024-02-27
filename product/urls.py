from django.urls import path
from .views import BuyItemView, InfoItemView

urlpatterns = [
    path("buy/<int:pk>", BuyItemView.as_view(), name="buy"),
    path("item/<int:pk>", InfoItemView.as_view(), name="item"),
    ]
