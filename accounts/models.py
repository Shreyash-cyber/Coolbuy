from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE,)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.png', blank=False, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=75, blank=True)
    dob = models.DateField(blank=True, null=True)
    joined_date = models.DateTimeField(default=timezone.now,editable=False)
    update_at = models.DateTimeField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Address(models.Model):
    state_choice = [
        ('Andhra Pradesh','Andhra Pradesh'),
        ('Arunachal Pradesh','Arunachal Pradesh'),
        ('Assam','Assam'),
        ('Bihar','Bihar'),
        ('Chhattisgarh','Chhattisgarh'),
        ('Goa','Goa'),
        ('Gujarat','Gujarat'),
        ('Haryana','Haryana'),
        ('Himachal Pradesh','Himachal Pradesh'),
        ('Jharkhand','Jharkhand'),
        ('Karnataka','Karnataka'),
        ('Kerala','Kerala'),
        ('Madhya Pradesh','Madhya Pradesh'),
        ('Maharashtra','Maharashtra'),
        ('Manipur','Manipur'),
        ('Meghalaya','Meghalaya'),
        ('Mizoram','Mizoram'),
        ('Nagaland','Nagaland'),
        ('Odisha','Odisha'),
        ('Punjab','Punjab'),
        ('Rajasthan','Rajasthan'),
        ('Sikkim','Sikkim'),
        ('Tamil Nadu','Tamil Nadu'),
        ('Telangana','Telangana'),
        ('Tripura','Tripura'),
        ('Uttar Pradesh','Uttar Pradesh'),
        ('Uttarakhand','Uttarakhand'),
        ('West Bengal','West Bengal'),
        ('Jammu and Kashmir','Jammu and Kashmir'),
        ('Ladakh','Ladakh'),
        ('Delhi','Delhi'),
    ]
    eighteen_choice = {
        ('Yes','Yes'),
        ('No','No')
    }
    phoneNumberRegex = RegexValidator(regex = r"^\d{10}$")
    pincodeRegex = RegexValidator(regex = r"^\d{6}$")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    reciever_name = models.CharField(max_length=200, blank=False)
    phone_no = models.CharField(validators = [phoneNumberRegex], max_length = 10, blank=False)
    alt_phone_no = models.CharField(validators = [phoneNumberRegex], max_length = 10, blank=True)
    state = models.CharField(max_length=50, choices=state_choice, blank=False)
    pincode = models.CharField(validators = [pincodeRegex], max_length = 6, blank=False)
    eighteen = models.CharField(blank=False, choices=eighteen_choice, default='Yes', max_length=4 )
    city = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=500, blank=False)
    locality = models.CharField(max_length=300, blank=True)
    joined_date = models.DateTimeField(default=timezone.now,editable=False)
    update_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(("Default"), default=True)


    def __str__(self):
        return self.user.username

class notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    sending_date = models.DateTimeField(default=timezone.now,editable=False)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
