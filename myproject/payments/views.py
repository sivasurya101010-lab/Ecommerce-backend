from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response

from django.shortcuts import (get_object_or_404)

from orders.models import Order
from .models import Payment

import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get('order_id')

        order = get_object_or_404(Order,id=order_id,user=request.user)

        amount = int(order.total_amount * 100)

        razorpay_order = (client.order.create({"amount": amount,"currency": "INR","payment_capture": 1}))

        payment = Payment.objects.create(order=order,razorpay_order_id=razorpay_order['id'],amount=order.total_amount)

        return Response({"razorpay_order_id":razorpay_order["id"],"amount":amount,"currency":"INR","key":settings.RAZORPAY_KEY_ID})


class VerifyPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = {

            'razorpay_order_id':request.data.get('razorpay_order_id'),

            'razorpay_payment_id':request.data.get('razorpay_payment_id'),

            'razorpay_signature':request.data.get('razorpay_signature')
        }

        if not data['razorpay_order_id'] or not data['razorpay_payment_id'] or not data['razorpay_signature']:

            return Response({"error":"Payment details are required"},status=400)

        try:

            client.utility.verify_payment_signature(data)

            payment = get_object_or_404(Payment,razorpay_order_id=data['razorpay_order_id'],order__user=request.user)

            payment.status = 'SUCCESS'

            payment.razorpay_payment_id = (data['razorpay_payment_id'])

            payment.save()

            payment.order.status = 'PAID'

            payment.order.save()

            return Response({"message":"Payment successful"})

        except Exception:

            return Response({"error":"Payment verification failed"},status=400)
