from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.views import View

# Create your views here.

class Blogs(View):
    def get(self, request):
        blog_list = Blog.objects.order_by('-joined_date')
        return render(request, 'blogs.html',{'blog_list':blog_list})

class ReadBlogs(View):
    def get(self, request, title):
        blogs = Blog.objects.filter(urltitle=title)
        return render(request,'blogs_read.html', {'blogs':blogs})
