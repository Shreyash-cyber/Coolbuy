from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from products.models import Categories, Subcategories, Item
from .forms import *

# Create your views here.
class home(View):
    def get (self, request):
        category_list = Categories.objects.order_by('-joined_date')
        subcategory_list = Subcategories.objects.order_by('-update_at')[:9]
        return render (request, 'home.html', {'subcategory_list': subcategory_list, 'category_list': category_list})

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return render( request, 'activation_sent_success.html')

        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('accounts:home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('accounts:home')

def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                    return redirect('accounts:home')
                else:
                    request.session.set_expiry(1209600)
                    return redirect('accounts:home')
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:register')
    else:
        form = LoginForm()
        return render(request, "login.html", {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile(request, username):
    return render (request, 'my_account.html')

@login_required
def edit_profile(request, username):
    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:home')
    else:
        form = Profileform()
    return render(request, 'edit_profile.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class my_address(View):
    def get(self, request, username):
        address = Address.objects.filter(user=request.user)
        return render(request, 'my_address.html', {'user_address': address })

@login_required
def add_address(request, username):
    if request.method == 'POST':
        form = Addressform(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('accounts:home')
    else:
        form = Addressform()
    return render(request, 'add_address.html', {'form': form})

@login_required
def delete_address(request, id):
    address = Address.objects.filter(id=id)
    address.delete()
    return redirect('accounts:home')

@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, id=id)
    if request.method == 'POST':
        form = Addressform(request.POST, instance=address)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('accounts:home')
    else:
        form = Addressform(instance=address)
    template_name = 'address_edit.html'
    context = {
        'form': form,
        'Address': address,
    }
    return render(request, template_name, context)

@login_required
def set_default_address(request, id):
    Address.objects.filter(user=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)
    return redirect('accounts:home')

def return_policy(request):
    return render(request, 'return_policy.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms&condition.html')

def billing(request):
    return render(request, 'billing&shipping.html')
