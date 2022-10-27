from django import forms
from django.forms import ModelForm, Textarea, fields, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
import re
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from .models import *

class SignUpForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Inform a valid phone number.")
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    phone = forms.CharField(validators=[phone_regex], max_length=10, required=True,)
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email)
        if qs.exists():
            raise ValidationError('A user with this email address already exists')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        qs = User.objects.exclude(pk=self.instance.pk).filter(phone__iexact=phone)
        if qs.exists():
            raise ValidationError('A user with same phone number already exists')
        return phone


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, label='Remember Me',help_text='To stay login please check the box.',widget=forms.CheckboxInput(attrs={'class': 'box'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user doesn't exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("User no longer Active")
        return super(LoginForm,self).clean(*args,**kwargs)

class Profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'joined_date', 'updated_at']
        labels = {
            'dob':'Date Of Birth',
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }

class Addressform(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['user', 'joined_date', 'updated_at']
        labels = {
            'reciever_name':'Reciever Name',
            'phone_no':'Phone No',
            'alt_phone_no':'Alternate Phone No',
            'state':'State/Union Territory',
            'pincode':'Area Pincode',
            'eighteen':'Is reciever is 18+',
            'city':'City',
            'address':'Address',
            'locality':'Locality',
        }
        widgets = {
            'eighteen': forms.RadioSelect()
        }
