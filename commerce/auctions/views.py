from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from json import dumps
from datetime import datetime

from .models import User, Bid, Listing, Comment#, Watchlist

def add_watchlist(request):
    pass

def make_bid(request):
    pass

# html variables are included here in request
def listing(request, listing_id):
    l = Listing.objects.get(pk=listing_id)

    if (l.is_active == False):
        return HttpResponseRedirect(reverse("index"))

    info = listing_to_dict(l)

    # note to self: cannot change the url here
    return render(request, "auctions/listing.html", {
        'listing': info
    })

def create_listing(request):
    return render(request, "auctions/create_listing.html")

def listing_to_dict(l):
    info = {
        'title': l.title,
        'description': l.description,
        'image_url': l.image_url,
        'category': l.category,
        'bids': [],
        'id': l.id,
    }

    bids = Bid.objects.filter(listing=l)

    for b in bids:
        info['bids'].append({
            'timestamp': b.timestamp.strftime("%m/%d/%Y %H:%M:%S"),
            'price': "$" + str(b.price),
            'user': b.user.username
        })

    info['starting_bid'] = info['bids'][0]
    info['current_bid'] = info['bids'][-1]
    return info

def index(request):
    all_listings = []
    for l in Listing.objects.all():
        if (l.is_active == False):
            continue

        info = listing_to_dict(l)
        print(info)
        print("\n\n\n")

        all_listings.append(info)

    return render(request, "auctions/index.html", {
        "listings": all_listings
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
            if request.POST["image_url"] != "":
                img = request.POST["image_url"]
            else:
                img = "https://www.actbus.net/fleetwiki/images/8/84/Noimage.jpg"

            l = Listing(
                title = request.POST["title"],
                description = request.POST['description'],
                image_url = img,
                category = request.POST["category"],
                is_active = 1,
            )

            l.valid()
            l.save()
            print(l)
            bid = Bid(
                price = float(request.POST["starting_bid"]), 
                user = request.user,
                listing = l,
            )
            bid.save()
            print(bid)



            return HttpResponseRedirect(reverse("index"))
        except:
            return render(request, "auctions/create_listing.html", {
                'message': "Please fill out all fields in the correct format.",
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