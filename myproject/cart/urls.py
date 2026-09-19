from django.urls import path
from .views import AddCartView, ItemCartView,ClearCartView,RemoveItemCartView,UpdateCartView


urlpatter=[
    path('cart/add/',AddCartView.as_view()),
    path('cart/',ItemCartView.as_view()),
    path('update/cart/<int:id>',UpdateCartView.as_view()),
    path('remove/item/cart/<int:id>',RemoveItemCartView.as_view()),
    path('delete/cart',ClearCartView.as_view()),
]