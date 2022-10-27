from django.conf.urls import url
from django.urls import path
from .views import *
from . import views
from .views import Blogs, ReadBlogs

# Template Urls!
app_name = 'blog'

urlpatterns = [
    path('blogs/',Blogs.as_view(),name="Blogs"),
    path('<slug:title>/',ReadBlogs.as_view(),name="readblog"),
]
