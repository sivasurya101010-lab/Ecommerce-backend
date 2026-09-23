from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Category,Product
from cart.models import Cart,CartItem
from .models import Order,OrderItem


class CheckoutTest(APITestCase):

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

    def test_checkout_without_login(self):
        response=self.client.post('/orders/checkout/')

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_checkout_empty_cart(self):
        self.client.force_authenticate(user=self.user)

        Cart.objects.create(user=self.user)

        response=self.client.post('/orders/checkout/')

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],'Cart is empty')
        self.assertEqual(Order.objects.count(),0)

    def test_checkout_order(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.post('/orders/checkout/')

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(),1)
        self.assertEqual(OrderItem.objects.count(),1)

        order=Order.objects.get(user=self.user)

        self.assertEqual(order.total_amount,'100000.00')
        self.assertEqual(order.status,'PENDING')
        self.assertEqual(order.items.first().quantity,2)
        self.assertEqual(order.items.first().price,'50000.00')

        self.product.refresh_from_db()

        self.assertEqual(self.product.stock,8)
        self.assertEqual(CartItem.objects.filter(cart=cart).count(),0)

    def test_checkout_more_than_stock(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=11
        )

        response=self.client.post('/orders/checkout/')

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('does not have enough stock',response.data['error'])

        self.assertEqual(Order.objects.count(),0)

        self.product.refresh_from_db()

        self.assertEqual(self.product.stock,10)

    def test_user_cannot_checkout_other_users_cart(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.other_user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.post('/orders/checkout/')

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(Order.objects.count(),0)


class MyOrdersTest(APITestCase):

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
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=50000
        )

    def test_get_my_orders(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.get('/orders/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['total_amount'],'50000.00')
        self.assertEqual(response.data[0]['status'],'PENDING')
        self.assertEqual(len(response.data[0]['items']),1)
        self.assertEqual(response.data[0]['items'][0]['product_name'],'Iphone')

    def test_user_does_not_see_other_users_orders(self):
        Order.objects.create(
            user=self.other_user,
            total_amount=70000
        )

        self.client.force_authenticate(user=self.user)

        response=self.client.get('/orders/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_get_order_detail(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.get(f'/orders/{self.order.id}/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['id'],self.order.id)
        self.assertEqual(response.data['total_amount'],'50000.00')
        self.assertEqual(response.data['items'][0]['product_name'],'Iphone')

    def test_user_cannot_view_other_users_order(self):
        other_order=Order.objects.create(
            user=self.other_user,
            total_amount=70000
        )

        self.client.force_authenticate(user=self.user)

        response=self.client.get(f'/orders/{other_order.id}/')

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
