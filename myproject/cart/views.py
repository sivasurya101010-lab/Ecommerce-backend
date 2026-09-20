from .seriaizers import CartItemSerialiser

from .models import Cart,CartItem
from products.models import Product

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404


class AddCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity')

        try:
            quantity=int(quantity)
        except (TypeError,ValueError):
            return Response({"error":"Quantity must be a valid number"},status=status.HTTP_400_BAD_REQUEST)

        if quantity<=0:
            return Response({"error":"Quantity must be at least 1"},status=status.HTTP_400_BAD_REQUEST)

        product=get_object_or_404(Product,id=product_id)

        if quantity>product.stock:
            return Response({"error":"out of stock"},status=status.HTTP_400_BAD_REQUEST)


        cart,created=Cart.objects.get_or_create(user=request.user)
        cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product)

        if not created:

            if cart_item.quantity+quantity>product.stock:
                return Response({"error":"Not enough stocks"},status=status.HTTP_400_BAD_REQUEST)

            cart_item.quantity+=quantity

        else:
            cart_item.quantity=quantity

        cart_item.save()

        return Response({"message": "Item added to cart"},status=status.HTTP_200_OK)



class ItemCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        cart,created=Cart.objects.get_or_create(user=request.user)

        items=cart.items.all()  #reverse relation

        serializer=CartItemSerialiser(items,many=True)

        total=0

        for item in items:
            total+=item.product.price*item.quantity

        return Response({'items':serializer.data,'total':total})


class UpdateCartView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request,id):

        try:
            quantity=int(request.data.get('quantity'))
        except (TypeError,ValueError):
            return Response({"error":"Quantity must be a valid number"},status=status.HTTP_400_BAD_REQUEST)

        if quantity<=0:
            return Response({"error":"Add minimum 1 item to the cart"},status=status.HTTP_400_BAD_REQUEST)

        item=get_object_or_404(CartItem,id=id,cart__user=request.user)

        if quantity>item.product.stock:
            return Response({"error":"Not enough stocks"},status=status.HTTP_400_BAD_REQUEST)

        item.quantity=quantity

        item.save()

        return Response({"message":"Cart updated"})


class RemoveItemCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request,id):
        item=get_object_or_404(CartItem,id=id,cart__user=request.user)

        item.delete()

        return Response({"message":"Item removed"})


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        cart=Cart.objects.filter(user=request.user).first()

        if cart:
            items=cart.items.all() #reverse relation
            items.delete()

        return Response({"message": "Cart cleared"})

