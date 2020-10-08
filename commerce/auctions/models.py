from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    bid = models.ForeignKey(Bid, on_delete=models.PROTECT)
    image = models.CharField(max_length=64, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)