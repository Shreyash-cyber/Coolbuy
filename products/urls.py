from os import name
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Product, Product_detail
from . import views


app_name = 'products'

urlpatterns = [
    path('<int:subcategory_id>/products/',Product.as_view(),name='product' ),
    path('<int:item_id>/details',Product_detail.as_view(),name='detail'),
    path('search-result/',views.search_item,name='search')
]