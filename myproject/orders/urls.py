from django.urls import path
from .views import MyOrdersView,MyordersDetailView,CheckoutView

urlpatterns=[
    path('checkout/',CheckoutView.as_view()),
    path('',MyOrdersView.as_view()),
    path('<int:id>/',MyordersDetailView.as_view()),
]
