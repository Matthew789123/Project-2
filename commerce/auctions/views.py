from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers

from .models import User, Listing, Bid, Category, Watchlist


def index(request):
    if request.user.is_authenticated:
        Watchlist.objects.get_or_create(user=request.user)
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "POST":
        if not request.POST["category"] is "":
            category = Category.objects.get(name=request.POST["category"])
        else:
            category = None
        listing = Listing(title=request.POST["title"], description=request.POST["description"], starting=request.POST["value"], image=request.POST["image"], category=category, user=request.user)
        listing.save()
        return HttpResponseRedirect(f"/{listing.pk}")
    return render(request, "auctions/create.html", {
        "Category" : Category.objects.values()
    })

def listing(request, id):
    message = None
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        if listing.bid is not None:
            if float(request.POST["value"]) > listing.bid.value:
                bid = Bid(user=request.user, value=request.POST["value"])
                bid.save()
                Bid.objects.get(id=listing.bid.pk).delete()
                listing.bid = bid
                listing.save()
            else:
                message = "Your bid is too low."
        else:
            if float(request.POST["value"]) >= listing.starting:
                bid = Bid(user=request.user, value=request.POST["value"])
                bid.save()
                listing.bid = bid
                listing.save()
            else:
                message = "Your bid is too low."
    return render(request, "auctions/listing.html", {
        "listing" : Listing.objects.get(id=id),
        "watchlist" : Watchlist.objects.get(user=request.user).item.all(),
        "message" : message
    })

def add(request, id):
    listing = Listing.objects.get(id=id)
    if Watchlist.objects.filter(user=request.user, item=id).exists():
        return HttpResponseRedirect(f"/{listing.pk}")
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    user_list.item.add(listing)
    return HttpResponseRedirect(f"/{listing.pk}")

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist" : Watchlist.objects.get(user=request.user).item.all()
    })

def remove(request, id):
    Watchlist.objects.get(user=request.user).item.remove(Listing.objects.get(id=id))
    return HttpResponseRedirect(reverse("watchlist"))