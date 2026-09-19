from .models import Order,OrderItem
from products.models import Product
from cart.models import Cart

from .serializers import OrderItemSerialiZer,OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction

class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        with transaction.atomic():

            cart = get_object_or_404(Cart,user=request.user)

            cart_items = cart.items.all()

            if not cart_items.exists():

                return Response({"error":"Cart is empty"},status=400)

            total = 0

            for item in cart_items:

                product = Product.objects.select_for_update().get(id=item.product.id)

                if item.quantity > product.stock:

                    return Response({"error":f"{product.name} does not have enough stock"},status=400)

                total += (product.price * item.quantity)

            order = Order.objects.create(user=request.user,total_amount=total)

            for item in cart_items:

                product = Product.objects.select_for_update().get(id=item.product.id)

                OrderItem.objects.create(order=order,product=product,quantity=item.quantity,price=product.price)

                product.stock -= item.quantity

                product.save()

            cart_items.delete()

            serializer = OrderSerializer(order)

            return Response(serializer.data,status=201)

class MyOrdersView(APIView):
    permission_classes=[IsAuthenticated]


    def get(self,request):
        orders=Order.objects.filter(user=request.user)

        serializer=OrderSerializer(orders,many=True)

        return Response(serializer.data)
    

    
class MyordersDetailView(APIView):

    authentication_classes=[IsAuthenticated]

    def get(self,request,id):
        order=get_object_or_404(Order,id=id)

        serializer=OrderSerializer(order)
