from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import ModelState
from django.db.models.fields import CharField, TextField
from django.utils import timezone
# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100, blank=False)
    joined_date = models.DateTimeField(default=timezone.now,editable=False)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Subcategories(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='our_categories')
    name = models.CharField(max_length=200, blank=False)
    joined_date = models.DateTimeField(default=timezone.now,editable=False)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    auth = [
        ('✔','✔'),
        ('✖','✖')
    ]
    rating = [
        ('⭐','⭐'),
        ('⭐⭐','⭐⭐'),
        ('⭐⭐⭐','⭐⭐⭐'),
        ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
        ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
    ]

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='our_items')
    subcategories = models.ForeignKey(Subcategories, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, blank=False)
    contain_size = models.CharField(max_length=50, blank=True)
    brand_name = models.CharField(max_length=100, blank=False, default='Bagh')
    swag = models.BooleanField(blank=False, default=False)
    male = models.BooleanField(blank=False, default=False)
    female = models.BooleanField(blank=False, default=False)
    unisex = models.BooleanField(blank=False, default=False)
    first = models.ImageField(upload_to='items', blank=False)
    second = models.ImageField(upload_to='items', blank=False)
    third = models.ImageField(upload_to='items', blank=True)
    fourth = models.ImageField(upload_to='items', blank=True)
    fifth = models.ImageField(upload_to='items', blank=True)
    sixth = models.ImageField(upload_to='items', blank=True)
    seventh = models.ImageField(upload_to='items', blank=True)
    rate = models.CharField(max_length=5, choices=rating, default='⭐⭐⭐⭐')
    taken_from = models.URLField(blank=False)
    color = models.CharField(max_length=30, blank=False, default='Black')
    material = models.CharField(max_length=50, blank=False, default='Plastic' )
    return_policy = models.CharField(max_length=100, blank=False, default='7Days Return Policy')
    stock = models.CharField(max_length=50, blank=False, default='In Stock')
    authentic = models.CharField(max_length=1,blank=False,choices=auth, default='✔')
    price = models.FloatField(blank=False,)
    actual_price = models.FloatField(blank=False)
    type = models.CharField(blank=False, max_length=100, default='Cloth')
    about = models.CharField(blank=False,max_length=100, default='Washable')
    offer = models.CharField(max_length=4, blank=True)
    joined_date = models.DateTimeField(default=timezone.now,editable=False)
    update_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    
    @staticmethod
    def get_items_by_id(ids):
        return Item.objects.filter(id__in = ids)

    def __str__(self):
        return self.name
