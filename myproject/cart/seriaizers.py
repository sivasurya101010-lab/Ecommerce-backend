from .models import Cart,CartIteam
from rest_framework import serializers

class CartItemSerialiser(serializers.ModelSerializer):

    price=serializers.DecimalField(source='product.price',read_only=True,max_digits=10,decimal_places=2)
    name=serializers.CharField(source='product.name',read_only=True)
    total_price = serializers.SerializerMethodField()

    class meta:
        model=CartIteam
        fields=['id','name','price','quantity','tota_price','product']

        def get_total_price(self,value):

            return (value.price*value.quantity)
