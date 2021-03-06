from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#         Token.objects.get_or_create(user=instance)
#         print(token.key)
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)

# Create your models here.
class Restaurant(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='restaurant')
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='customer')
    avatar = models.ImageField(upload_to='customer_profile/', blank=True)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()


# this model Stores the data of the Phones Verified
class phoneModel(models.Model):
    Mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)   # For HOTP Verification

    def __str__(self):
        return str(self.Mobile)

        

class Driver(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='driver')
    avatar = models.ImageField(upload_to='driver_profile/', blank=True)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class Category(models.Model):
    name = models.CharField(max_length=90, unique=True)
    category_image = models.ImageField(upload_to='category_images/', blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', blank=True)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='meal_images/', blank=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cooking"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, blank=True, null=True, on_delete=models.CASCADE)  # can be blank
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    picked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)