from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)

class Category(models.Model):
    name = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.CharField(max_length=512, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    opened = models.BooleanField(default=True)

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    item = models.ManyToManyField(Listing)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)