from django.db import models
from orders.models import Order

class Payment(models.Model):

    status_choices=[('PENDING','pending'),('SUCCESS','success'),('FAILED','failed')]

    order=models.OneToOneField(Order,on_delete=models.CASCADE)

    razorpay_order_id=models.CharField(max_length=255,unique=True)

    razorpay_payment_id=models.CharField(max_length=255,blank=True,null=True)

    amount=models.DecimalField(max_digits=10,decimal_places=2)

    created_at=models.DateField(auto_now_add=True)

    status=models.CharField(max_length=20,choices=status_choices,default='PENDING')

    def __str__(self):
        return self.razorpay_order_id
