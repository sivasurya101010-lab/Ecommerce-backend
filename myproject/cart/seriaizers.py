from .models import CartItem
from rest_framework import serializers


class CartItemSerialiser(serializers.ModelSerializer):

    price = serializers.DecimalField(
        source='product.price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )

    name = serializers.CharField(source='product.name',read_only=True)

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'name', 'price', 'quantity', 'total_price', 'product']

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity