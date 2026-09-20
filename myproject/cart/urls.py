from django.urls import path
from .views import AddCartView, ItemCartView,ClearCartView,RemoveItemCartView,UpdateCartView


urlpatterns=[
    path('add/',AddCartView.as_view()),
    path('',ItemCartView.as_view()),
    path('update/<int:id>/',UpdateCartView.as_view()),
    path('remove/<int:id>/',RemoveItemCartView.as_view()),
    path('clear/',ClearCartView.as_view()),
]

