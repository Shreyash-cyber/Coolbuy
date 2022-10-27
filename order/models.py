from random import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Item
from accounts.models import Address

# Create your models here.
class Order(models.Model):
    status_choices = (
        (1, 'PENDING'),
        (2, 'CONFIRMED'),
        (3, 'PACKED'),
        (4, 'SHIPPED'),
        (5, 'IN WAY'),
        (6, 'ARRIVED DESTINATION'),
        (7, 'RECIEVED'),
        (8, 'COMPLETED')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    address = models.ForeignKey(Address, default= True, on_delete=models.CASCADE)
    status = models.IntegerField(choices = status_choices, default=1)
    method = models.CharField(max_length=50, blank=False,)
    total_price = models.FloatField(blank=False, default=0)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=200, null=True, default=None) 
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    created_at = models.TimeField(auto_now=True, editable=False)
    razorpay_order_id = models.CharField(max_length=1000, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=1000, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username + " " + str(self.order_id)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment:
            self.order_id = self.datetime_of_payment.strftime('COOLBUYORDER%Y%m%dODR%H%M%S') 
        return super(Order,self).save(*args, **kwargs)
            

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_item')
    item = models.ForeignKey(Item, on_delete=models.CASCADE )
    size = models.CharField(max_length=20, blank=False)
    price = models.FloatField(blank=False)
    
    
    def __str__(self):
        return self.order.order_id