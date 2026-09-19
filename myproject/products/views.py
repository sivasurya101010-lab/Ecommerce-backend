from django.shortcuts import render
from rest_framework import generics
from .models import Category,Product
from .serialiser import CategorySerializer,ProductSerializer
from rest_framework.permissions import IsAdminUser,AllowAny

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        
        return [AllowAny()]
    

    
class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]

    filterset_fields=['category','is_available']
    search_fields=['name','description']
    ordering_fields=['price','created_at']

    def get_queryset(self):
        queryset=Product.objects.all()

        max_price=self.request.query_params.get('max_price')
        min_price=self.request.query_params.get('min_price')

        if max_price:
            queryset=Product.objects.filter(price__lte=max_price)

        if min_price:
            queryset=Product.objects.filter(price__gte=min_price)
        
        return queryset



    def get_permissions(self):
        if self.request.method=='POST':
            return[IsAdminUser()]
        
        return[AllowAny()]


class ProductDetailView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer



class ProductEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer