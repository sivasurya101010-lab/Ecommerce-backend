from django.urls import path
from .views import MyOrdersView,MyordersDetailView,CheckoutView

urlpatterns=[
    path('orders/checkout/',CheckoutView.as_view()),
    path('orders/orders/',MyOrdersView.as_view()),
    path('orders/ordersdetail/',MyordersDetailView.as_view()),
]
