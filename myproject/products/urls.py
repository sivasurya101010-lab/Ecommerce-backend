from .views import CategoryView,ProductDetailView,ProductListView,ProductEditView
from django.urls import path

urlpatterns=[
        path('categories/',CategoryView.as_view()),
        path('edit/[int:pk](int:pk)/',ProductEditView.as_view()),
        path('',ProductListView.as_view()),
        path('[int:pk](int:pk)/',ProductDetailView.as_view()),

]
