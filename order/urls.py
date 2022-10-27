from os import name
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Cart, Checkout_Post, Checkout_Pre, Myorder
from . import views

# Template Urls!
app_name = 'orders'

urlpatterns = [
    path('cart/', Cart.as_view(),name='cart'),
    path('Check-Out/PlaceCod', Checkout_Post.as_view(),name='checkout-post'),
    path('OrderSuccess/', views.successcash, name='successcod'),
    path('PlaceInstantly', Checkout_Pre.as_view(),name='checkout'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
    path('my_orders/', Myorder.as_view(),name='myorders'),
]