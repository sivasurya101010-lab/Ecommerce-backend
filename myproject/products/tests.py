from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category,Product


class CategoryTest(APITestCase):

    def setUp(self):
        self.admin=User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )

    def test_get_categories(self):
        Category.objects.create(name='Mobiles')

        response=self.client.get('/products/categories/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['name'],'Mobiles')

    def test_admin_can_create_category(self):
        self.client.force_authenticate(user=self.admin)

        response=self.client.post('/products/categories/',{
            'name':'Mobiles',
            'description':'Mobile phones'
        })

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name='Mobiles').exists())

    def test_normal_user_cannot_create_category(self):
        user=User.objects.create_user(
            username='surya',
            password='surya12345'
        )

        self.client.force_authenticate(user=user)

        response=self.client.post('/products/categories/',{
            'name':'Mobiles'
        })

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


class ProductTest(APITestCase):

    def setUp(self):
        self.admin=User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )
        self.user=User.objects.create_user(
            username='surya',
            password='surya12345'
        )
        self.category=Category.objects.create(name='Mobiles')
        self.product=Product.objects.create(
            category=self.category,
            name='Iphone',
            price=50000,
            description='Apple phone',
            stock=10
        )

    def test_get_products(self):
        response=self.client.get('/products/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['name'],'Iphone')

    def test_get_product_detail(self):
        response=self.client.get(f'/products/{self.product.id}/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],'Iphone')
        self.assertEqual(response.data['stock'],10)

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin)

        response=self.client.post('/products/',{
            'category':self.category.id,
            'name':'Laptop',
            'price':'70000.00',
            'description':'Gaming laptop',
            'stock':5,
            'is_available':True
        })

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Laptop').exists())

    def test_normal_user_cannot_create_product(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.post('/products/',{
            'category':self.category.id,
            'name':'Laptop',
            'price':'70000.00',
            'description':'Gaming laptop',
            'stock':5,
            'is_available':True
        })

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_product(self):
        self.client.force_authenticate(user=self.admin)

        response=self.client.put(f'/products/edit/{self.product.id}/',{
            'category':self.category.id,
            'name':'Iphone 15',
            'price':'60000.00',
            'description':'Updated phone',
            'stock':8,
            'is_available':True
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name,'Iphone 15')
        self.assertEqual(self.product.stock,8)

    def test_normal_user_cannot_update_product(self):
        self.client.force_authenticate(user=self.user)

        response=self.client.patch(f'/products/edit/{self.product.id}/',{
            'name':'Changed'
        })

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_product(self):
        self.client.force_authenticate(user=self.admin)

        response=self.client.delete(f'/products/edit/{self.product.id}/')

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_product_search(self):
        Product.objects.create(
            category=self.category,
            name='Samsung Phone',
            price=30000,
            description='Android phone',
            stock=5
        )

        response=self.client.get('/products/?search=Samsung')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['name'],'Samsung Phone')

    def test_product_min_price_filter(self):
        Product.objects.create(
            category=self.category,
            name='Cheap Phone',
            price=10000,
            stock=5
        )

        response=self.client.get('/products/?min_price=40000')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['name'],'Iphone')

    def test_product_max_price_filter(self):
        Product.objects.create(
            category=self.category,
            name='Cheap Phone',
            price=10000,
            stock=5
        )

        response=self.client.get('/products/?max_price=40000')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['name'],'Cheap Phone')

    def test_product_ordering(self):
        Product.objects.create(
            category=self.category,
            name='Cheap Phone',
            price=10000,
            stock=5
        )

        response=self.client.get('/products/?ordering=price')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Cheap Phone')
        self.assertEqual(response.data[1]['name'],'Iphone')
