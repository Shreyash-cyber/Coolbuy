from django.contrib import admin
from .models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):

    search_fields = ['user', 'order_id', 'datetime_of_payment']

    list_filter = ['status', 'payment_status', 'method']

    list_display =  ['user', 'order_id', 'method', 'payment_status', 'status','datetime_of_payment']


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)