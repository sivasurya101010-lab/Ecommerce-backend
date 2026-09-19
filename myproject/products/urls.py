from .views import CategoryView,ProductDetailView,ProductListView,ProductEditView
from django.urls import path

urlpatterns=[
    path('categories/',CategoryView.as_view()),
    path('productEdit/',ProductEditView.as_view()),
    path('productList/',ProductListView.as_view()),
    path('productDetail/',ProductDetailView.as_view()),

]