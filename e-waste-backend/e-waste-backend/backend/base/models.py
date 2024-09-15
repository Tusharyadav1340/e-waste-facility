from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .managers import CustomUserManager
from django.core.validators import RegexValidator

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


def upload_to(instance, filename):
    return 'base/images/{filename}'.format(filename=filename)

def uploadproduct(instance, filename):
    return 'base/images/{filename}'.format(filename=filename)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_CHOICES=[
        ('employee','Employee'),
        ('sub_employee','Sub-employee'),
        ('baseUser','User'),
    ]
    email        = LowercaseEmailField(_('email address'), unique=True)
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    date_joined  = models.DateTimeField(default=timezone.now)
    admin        = models.BooleanField(default=False)
    username     = models.CharField(max_length=12)
    user_image   = models.ImageField(upload_to=upload_to, default="")
    phone_regex  = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone        = models.CharField(default="",max_length=255, validators=[phone_regex], blank = True, null=True)
    house        = models.CharField(default="",max_length=255,blank = True, null=True)
    area         = models.CharField(default="",max_length=255,blank = True, null=True)
    landmark     = models.CharField(default="",max_length=255,blank = True, null=True)
    pincode      = models.CharField(default="",max_length=6,blank = True, null=True)
    town         = models.CharField(default="",max_length=255,blank = True, null=True)
    state        = models.CharField(default="",max_length=255,blank = True, null=True)
    country      = models.CharField(default="",max_length=255,blank = True, null=True)
    user_choices = models.TextField(choices=USER_CHOICES,blank = True, null=True)
    total_coins  = models.IntegerField(null=True)
    total_recycle = models.IntegerField(null=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class UserProducts(models.Model):
    TYPES_CHOICES = [
        ('Phone', 'Phone'),
        ('Headset', 'Headset'),
        ('Laptop', 'Laptop'),
        ('Mixer', 'Mixer'),
        ('Refrigerator', 'Refrigerator'),
        ('Speaker', 'Speaker'),
        ('Television', 'Television'),
        ('Washing Machine', 'Washing Machine')
    ]
    
    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Worst', 'Worst')
    ]
    STATUS_CHOICES = [
        ('None', 'None'),
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    user           = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    model          = models.CharField(max_length=100, default='',blank=True,null=True)
    manufacturer   = models.CharField(max_length=100, default='',blank=True,null=True)
    product_type   = models.CharField(choices=TYPES_CHOICES, max_length=20, default='',blank=True,null=True) 
    condition      = models.CharField(choices=CONDITION_CHOICES, max_length=20, default='',blank=True,null=True)  
    metal_quantity = models.JSONField(default=str,blank=True,null=True) 
    coins          = models.IntegerField(default=0,blank=True,null=True)
    product_image  = models.ImageField(upload_to=uploadproduct, default="",blank=True,null=True)
    status         = models.CharField(choices=STATUS_CHOICES, max_length=20, default='',blank=True,null=True) 
    created_on     = models.DateTimeField(auto_now=True)
    orderno        = models.CharField(max_length=30,blank=True,default='',null=True)
    transaction_no = models.CharField(max_length=30,blank=True,default='',null=True)


class Education(models.Model):
    title       = models.CharField(max_length=200)
    content1    = models.TextField(blank=True)
    content2    = models.TextField(blank=True)
    content3    = models.TextField(blank=True)
    content4    = models.TextField(blank=True)
    content5    = models.TextField(blank=True)
    content6    = models.TextField(blank=True)
    author      = models.CharField(max_length=100)
    created_on  = models.DateTimeField(auto_now=True, null=True)
    image       = models.ImageField(upload_to='backend',default="",blank=True,null=True)

class Facility(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

class Coupon(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='coupon', blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    terms = models.TextField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class CouponRedemption(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('coupon','user')

    def __str__(self):
        return f"{self.user.username} redeemed {self.coupon.code} on {self.redeemed_at}"
    


class Transaction(models.Model):
    user   = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True, related_name = 'transaction_user')
    seller = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True, related_name = 'transaction_seller')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(UserProducts,on_delete=models.CASCADE, null=True)
    time   = models.DateTimeField(auto_now_add=True)
    coins  = models.PositiveIntegerField()
    credit = models.BooleanField(default=True)