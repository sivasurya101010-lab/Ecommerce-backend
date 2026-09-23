from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Category,Product
from .models import Cart,CartItem


class CartTest(APITestCase):

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

    def test_user_cannot_add_to_cart_without_login(self):
        response=self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':1
        })

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_user_can_add_product_to_cart(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':2
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        cart=Cart.objects.get(user=self.user)
        item=CartItem.objects.get(cart=cart,product=self.product)

        self.assertEqual(item.quantity,2)

    def test_add_cart_invalid_quantity(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':'abc'
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'Quantity must be a valid number'
        )

    def test_add_cart_zero_quantity(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':0
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_add_cart_more_than_stock(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':11
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],'out of stock')

    def test_add_same_product_increases_quantity(self):
        self.client.force_authenticate(user=self.user)

        self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':2
        })

        response=self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':3
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        item=CartItem.objects.get(
            cart__user=self.user,
            product=self.product
        )

        self.assertEqual(item.quantity,5)

    def test_add_same_product_more_than_stock(self):
        self.client.force_authenticate(user=self.user)

        self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':7
        })

        response=self.client.post('/cart/add/',{
            'product_id':self.product.id,
            'quantity':4
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],'Not enough stocks')

    def test_get_cart(self):
        self.client.force_authenticate(user=self.user)

        Cart.objects.create(user=self.user)
        cart=Cart.objects.get(user=self.user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.get('/cart/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']),1)
        self.assertEqual(response.data['items'][0]['name'],'Iphone')
        self.assertEqual(response.data['items'][0]['quantity'],2)
        self.assertEqual(str(response.data['items'][0]['total_price']),'100000.00')
        self.assertEqual(str(response.data['total']),'100000.00')

    def test_update_cart_item(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.user)

        item=CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.patch(f'/cart/update/{item.id}/',{
            'quantity':5
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        item.refresh_from_db()

        self.assertEqual(item.quantity,5)

    def test_update_cart_invalid_quantity(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.user)

        item=CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.patch(f'/cart/update/{item.id}/',{
            'quantity':'abc'
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_update_cart_more_than_stock(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.user)

        item=CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.patch(f'/cart/update/{item.id}/',{
            'quantity':11
        })

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],'Not enough stocks')

    def test_user_cannot_update_other_users_cart_item(self):
        self.client.force_authenticate(user=self.user)

        other_cart=Cart.objects.create(user=self.other_user)

        item=CartItem.objects.create(
            cart=other_cart,
            product=self.product,
            quantity=2
        )

        response=self.client.patch(f'/cart/update/{item.id}/',{
            'quantity':5
        })

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_remove_cart_item(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.user)

        item=CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.delete(f'/cart/remove/{item.id}/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_user_cannot_remove_other_users_item(self):
        self.client.force_authenticate(user=self.user)

        other_cart=Cart.objects.create(user=self.other_user)

        item=CartItem.objects.create(
            cart=other_cart,
            product=self.product,
            quantity=2
        )

        response=self.client.delete(f'/cart/remove/{item.id}/')

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertTrue(CartItem.objects.filter(id=item.id).exists())

    def test_clear_cart(self):
        self.client.force_authenticate(user=self.user)

        cart=Cart.objects.create(user=self.user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        response=self.client.delete('/cart/clear/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.filter(cart=cart).count(),0)

    def test_get_cart_for_user_without_cart(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.get('/cart/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['items'],[])
        self.assertEqual(str(response.data['total']),'0')


class CartSerializerTest(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(
            username='surya',
            password='surya12345'
        )
        self.category=Category.objects.create(name='Mobiles')
        self.product=Product.objects.create(
            category=self.category,
            name='Iphone',
            price=50000,
            stock=10
        )

    def test_cart_item_serializer(self):
        from .seriaizers import CartItemSerialiser

        cart=Cart.objects.create(user=self.user)

        item=CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=3
        )

        serializer=CartItemSerialiser(item)

        self.assertEqual(serializer.data['name'],'Iphone')
        self.assertEqual(serializer.data['price'],'50000.00')
        self.assertEqual(serializer.data['quantity'],3)
        self.assertEqual(serializer.data['total_price'],'150000.00')
