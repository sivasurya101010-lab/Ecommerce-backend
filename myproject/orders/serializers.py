from rest_framework import serializers
from .models import Order,OrderItem

class OrderItemSerialiZer(serializers.ModelSerializer):

    product_name=serializers.CharField(source='product.name',read_only=True)

    class Mets:
        model=OrderItem
        fields = ['id','product_name','quantity','price']
        

class OrderSerializer(serializers.ModelSerializer):

    items=OrderItemSerialiZer(many=True,read_only=True)

    class Meta:
        model=Order
        
        fields = ['id','total_amount','status','created_at','items' ]