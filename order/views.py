from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
from django.utils.encoding import force_bytes, force_text
from django.db import transaction
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.template.loader import get_template
import os
from coolbuy import settings
from accounts.models import *
from products.models import *
from .models import *
from django.views import View
import razorpay

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Cart(View):
    def get (self, request): 
        cart = request.session.get('cart', None)
        if not cart:
            cart = {}
        request.session['cart'] = cart
        ids = (list(cart.keys()))
        ids = (list(request.session.get('cart').keys()))
        item = Item.get_items_by_id(ids)
        address = Address.objects.filter(user=request.user, default=True)
        print(item)
        return render(request, 'cart.html', {'items': item, 'addresses':address })

@method_decorator(login_required, name='dispatch')
class Wish(View):
    def get (self, request): 
        wish = request.session.get('wish', None)
        if not wish:
            wish = {}
        request.session['wish'] = wish
        ids = (list(wish.keys()))
        ids = (list(request.session.get('wish').keys()))
        item = Item.get_items_by_id(ids)
        address = Address.objects.filter(user=request.user, default=True)
        print(item)
        return render(request, 'wish.html', {'items': item, 'addresses':address })

@method_decorator(login_required, name='dispatch')
class Checkout_Post(View):
    def post (self, request,):
        user = request.user
        address = Address.objects.filter(default=True, user=request.user)
        cart = request.session.get('cart')
        items = Item.get_items_by_id(list(cart.keys()))
        prefer = request.POST.get('payment')
        total_price = request.POST.get('paying_price')
        total_item_price = json.loads(total_price)
        with transaction.atomic():
            order = Order.objects.create(
                    user=user,
                    total_price=total_price,
                    address=address.first(),
                    method = prefer,
                    )
            for item in items:
                item_order = OrderItem.objects.create(
                    order=order,
                    item=item,
                    size=cart.get(str(item.id)),
                    price=item.price,
                )        
            request.session['cart'] = {}
        return render(request , 'payment/cashondeliversummary.html',{'order':order, 'orderId':order.order_id, 'final_price':total_item_price,})

@login_required
def successcash(request):
    return render(request, 'payment/successcod.html')

# adding payment gateway
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

@method_decorator(login_required, name='dispatch')
class Checkout_Pre(View):
    def post (self, request,):
        user = request.user
        address = Address.objects.filter(default=True, user=request.user)
        cart = request.session.get('cart')
        items = Item.get_items_by_id(list(cart.keys()))
        prefer = request.POST.get('payment')
        total_price = request.POST.get('paying_price')
        total_item_price = json.loads(total_price)
        with transaction.atomic():
            order = Order.objects.create(
                    user=user,
                    total_price=total_item_price,
                    address=address.first(),
                    method = prefer,
                    )
            for item in items:
                item_order = OrderItem.objects.create(
                    order=order,
                    item=item,
                    size=cart.get(str(item.id)),
                    price=item.price,
                    )   
        order_currency = 'INR'
    
        callback_url = 'http://'+ str(get_current_site(request))+'/handlerequest/'
        print(callback_url)
        notes = {'order-type': "Basic order from the coolbuy website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=total_item_price*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
               
        return render(request, 'payment/razorpaypaymentsummary.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':total_item_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url,})

@csrf_exempt
def handlerequest(request):
    cart = request.session.get('cart')
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 not found please revisit the site")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result==None:
                amount = order_db.total_price * 100   #we have to pass in paisa
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.status = 2
                    order_db.save()
                    request.session['cart'] = {}
                    return render(request, 'payment/paymentsuccess.html',{'id':order_db.id})
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'payment/paymentfailed.html')
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'payment/paymentfailed.html')
        except:
            return HttpResponse("505 not found please revisit the site ")

@method_decorator(login_required, name='dispatch')
class Myorder(View):
    def get (self, request):
        order = Order.objects.filter(user=request.user)
        return render(request, 'my_order.html', {'user_order': order })

@method_decorator(login_required, name='dispatch')
class detail_order(View):
    def get (self, request, id):
        order = Order.objects.filter(id=id)
        return render(request, 'order_Detail.html', {'order': order})