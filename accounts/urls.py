from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import my_address, home , SignUpView, ActivateAccount
from . import views


app_name = 'accounts'

urlpatterns = [
    path('',home.as_view(),name='home' ),
    path('login/',views.my_login,name='login'),
    path('register/',SignUpView.as_view(),name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('@<slug:username>/',views.profile, name='profile'),
    path('@<slug:username>/edit-profile/',views.edit_profile,name='edit'),
    path('@<slug:username>/address',my_address.as_view(),name='address'),
    path('@<slug:username>/add-address',views.add_address,name='add_address'),
    path('<int:id>/delete-address',views.delete_address,name='delete_address'),
    path('<int:id>/edit-address',views.edit_address,name='edit_address'),
    path('<int:id>/set-default',views.set_default_address,name='default-address'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('privacy/',views.privacy,name='privacy'),
    path('return-policy/',views.return_policy, name='return'),
    path('terms-&-condition/',views.terms, name='terms'),
    path('billing-shipping-policy/',views.billing, name='billing'),
]
