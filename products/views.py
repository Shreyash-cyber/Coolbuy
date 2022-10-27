from os import name
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.views.generic import detail
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ValidationError
from django.views import View
from django.utils.decorators import method_decorator
from .models import Item, Categories, Subcategories
# Create your views here.
class Product(View):
    def get(self, request, subcategory_id):
        subcategory = get_object_or_404(Subcategories, pk=subcategory_id)

        sort_by = request.GET.get("sort", "l2h") 
        if sort_by == "l2h":
           products = subcategory.products.order_by("price")
        elif sort_by == "h2l":
           products = subcategory.products.order_by("-price")
        sort_by = request.GET.get("sort", "newest")
        if sort_by == "unisex":
            products = subcategory.products.order_by("-unisex")
        elif sort_by == "newest":
            products = subcategory.products.order_by("-update_at")
        sort_by = request.GET.get("sort", "male")
        if sort_by == "male":
            products = subcategory.products.order_by("-male")
        elif sort_by == "female":
            products = subcategory.products.order_by("-female")

        category_list = Categories.objects.all()
        return render (request, 'products.html',{"subcategory_list" : products, 'category_list': category_list })

class Product_detail(View):
    def get(self, request, item_id,):
        item = Item.objects.filter(id=item_id)
        category_list = Categories.objects.all()
        items = Item.objects.order_by('-update_at')
        return render (request, 'product_detail.html',{"items" : item, 'category_list': category_list, 'item': items })
    
    def post(self, request, item_id):
        item = request.POST.get('item')
        size = request.POST.get('Size')
        cart = request.session.get('cart')
        if cart:
            cart[item] = size
        else:
            cart = {}
            cart[item] = size
        request.session['cart'] = cart
        print(cart)
        return redirect('products:detail', item_id=item_id)
    
def search_item(request):
    search_item = request.GET.get('search')
    if search_item:
        items = Item.objects.filter(Q(name__icontains=search_item)|Q(color__icontains=search_item)|Q(material__icontains=search_item)|Q(type__icontains=search_item))
    return render(request, 'search_result.html', {'items':items})