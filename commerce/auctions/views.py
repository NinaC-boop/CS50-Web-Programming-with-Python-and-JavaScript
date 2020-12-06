from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Bid, Listing, Comment#, Watchlist

def create_listing(request):
    return render(request, "auctions/create_listing.html")

def index(request):
    print(list(Bid.objects.all()))
    print(list(Bid.objects.all()))
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "all_bids": Bid.objects.all(),
    })

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

def create(request):
    if request.method == "POST":
        try:
            listing = Listing(
                title = request.POST["title"],
                description = request.POST['description'],
                image_url = request.POST["image_url"],
                category = request.POST["category"],
                is_active = 1,
            )
            listing.valid()
            listing.save()
            print(listing)
            bid = Bid(
                price = float(request.POST["starting_bid"]), 
                user = request.user,
                listing = listing,
            )
            bid.save()
            print(bid)



            return HttpResponseRedirect(reverse("index"))
        except:
            return render(request, "auctions/create_listing.html", {
                'message': "Please fill out all fields in the correct format",
            })

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