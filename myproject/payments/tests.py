from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from products.models import Category,Product
from orders.models import Order
from .models import Payment


class PaymentTest(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(
            username='surya',
            password='surya12345'
        )
        self.other_user=User.objects.create_user(
            username='other',
            password='other12345'
        )
        self.category=Category.objects.create(name='Mobiles')
        self.product=Product.objects.create(
            category=self.category,
            name='Iphone',
            price=50000,
            stock=10
        )
        self.order=Order.objects.create(
            user=self.user,
            total_amount=50000
        )

    def test_create_payment_without_login(self):
        response=self.client.post('/api/payments/create/',{
            'order_id':self.order.id
        })

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    @patch('payments.views.client.order.create')
    def test_create_payment(self,mock_create):
        mock_create.return_value={
            'id':'order_test_123'
        }

        self.client.force_authenticate(user=self.user)

        response=self.client.post('/api/payments/create/',{
            'order_id':self.order.id
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['razorpay_order_id'],'order_test_123')
        self.assertEqual(response.data['amount'],5000000)
        self.assertEqual(response.data['currency'],'INR')

        payment=Payment.objects.get(order=self.order)

        self.assertEqual(payment.razorpay_order_id,'order_test_123')
        self.assertEqual(payment.amount,'50000.00')
        self.assertEqual(payment.status,'PENDING')

    @patch('payments.views.client.order.create')
    def test_user_cannot_create_payment_for_other_users_order(self,mock_create):
        mock_create.return_value={
            'id':'order_test_123'
        }

        other_order=Order.objects.create(
            user=self.other_user,
            total_amount=70000
        )

        self.client.force_authenticate(user=self.user)

        response=self.client.post('/api/payments/create/',{
            'order_id':other_order.id
        })

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(Payment.objects.count(),0)

    def test_verify_payment_without_login(self):
        response=self.client.post('/api/payments/verify/',{})

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_verify_payment_without_details(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.post('/api/payments/verify/',{
            'razorpay_order_id':'order_test_123'
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'Payment details are required'
        )

    @patch('payments.views.client.utility.verify_payment_signature')
    def test_verify_payment(self,mock_verify):
        payment=Payment.objects.create(
            order=self.order,
            razorpay_order_id='order_test_123',
            amount=self.order.total_amount
        )

        self.client.force_authenticate(user=self.user)

        response=self.client.post('/api/payments/verify/',{
            'razorpay_order_id':'order_test_123',
            'razorpay_payment_id':'pay_test_123',
            'razorpay_signature':'signature_test'
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Payment successful')

        payment.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEqual(payment.status,'SUCCESS')
        self.assertEqual(payment.razorpay_payment_id,'pay_test_123')
        self.assertEqual(self.order.status,'PAID')

        mock_verify.assert_called_once()

    @patch('payments.views.client.utility.verify_payment_signature')
    def test_verify_payment_failed(self,mock_verify):
        mock_verify.side_effect=Exception()

        payment=Payment.objects.create(
            order=self.order,
            razorpay_order_id='order_test_123',
            amount=self.order.total_amount
        )

        self.client.force_authenticate(user=self.user)

        response=self.client.post('/api/payments/verify/',{
            'razorpay_order_id':'order_test_123',
            'razorpay_payment_id':'pay_test_123',
            'razorpay_signature':'wrong_signature'
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],'Payment verification failed')

        payment.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEqual(payment.status,'PENDING')
        self.assertEqual(self.order.status,'PENDING')

    @patch('payments.views.client.utility.verify_payment_signature')
    def test_user_cannot_verify_other_users_payment(self,mock_verify):
        other_order=Order.objects.create(
            user=self.other_user,
            total_amount=70000
        )

        Payment.objects.create(
            order=other_order,
            razorpay_order_id='other_order_123',
            amount=other_order.total_amount
        )

        self.client.force_authenticate(user=self.user)

        response=self.client.post('/api/payments/verify/',{
            'razorpay_order_id':'other_order_123',
            'razorpay_payment_id':'pay_test_123',
            'razorpay_signature':'signature_test'
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],'Payment verification failed')
