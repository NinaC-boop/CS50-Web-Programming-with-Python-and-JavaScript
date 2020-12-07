from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from json import dumps
from datetime import datetime

from .models import User, Bid, Listing, Comment, Watchlist

def category(request):
    ctgs = []
    category_listings = []
    for l in Listing.objects.all():
        if l.category != "" and l.category not in ctgs:
            ctgs.append(l.category)

            # all the listings in the same category
            listings = []
            for filtered_l in Listing.objects.filter(category=l.category):
                if filtered_l.is_active:
                    listings.append(listing_to_info_dict(filtered_l))

            if listings != []:
                category_listings.append({
                    'category': l.category,
                    'listings': listings,
                })
                
    return render(request, "auctions/category.html", {
        'category_listings': category_listings,
    })

def add_comment(request):
    if request.method == "POST":
        try:
            listing_id = request.POST["listing_id"]

            u = User.objects.get(username=request.POST["user"])
            c = Comment(
                comment = request.POST["new_comment"],
                user = u,
                listing = Listing.objects.get(pk=listing_id),
            )
            c.valid()
            c.save()

            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        except:
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def close_auction(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        l = Listing.objects.get(pk=listing_id)
        l.is_active = False
        l.save()
        info = listing_to_info_dict(l)

        return render(request, "auctions/closed_listing.html", {
        'listing': info,
        'watched': is_watched(l, request.user),
        'is_owner': info['bids'][0]['user'] == request.user.username,
        })

def is_watched(l, u):
    if not u.is_authenticated:
        return False
    if list(Watchlist.objects.filter(listing=l, user=u)) == []:
        return False
    return True

def add_watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        l = Listing.objects.get(pk=listing_id)
        u = request.user
        if not is_watched(l, u):
            w = Watchlist(
                user = u,
                listing = l,
            )
            w.save()
            print("added to watchlist")
        else:
            Watchlist.objects.filter(listing=l, user=u).delete()
            print("deleted from watchlist")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def make_bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]

        if request.POST["new_bid"] == "":
            messages.add_message(request, messages.ERROR, "Please enter a valid bid.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        new_bid = round(float(request.POST["new_bid"]), 2)

        
        l = Listing.objects.get(pk=listing_id)
        info = listing_to_info_dict(l)

        # bid is not at least as large as the starting bid
        # bid is not greater than any other bid
        if (info['current_bid']['price'] == info['starting_bid']['price'] and new_bid < float(info['starting_bid']['price'][1:])) or (info['current_bid']['price'] != info['starting_bid']['price'] and new_bid <= float(info['current_bid']['price'][1:])):
            messages.add_message(request, messages.ERROR, "Please enter a valid bid.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
        bid = Bid(
            price = new_bid,
            user = request.user,
            listing = l,
        )
        bid.save()

        print(bid)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# html variables are included here in request
def listing(request, listing_id):
    l = Listing.objects.get(pk=listing_id)
    info = listing_to_info_dict(l)

    if (l.is_active == False):
        return render(request, "auctions/closed_listing.html", {
        'listing': info,
        'watched': is_watched(l, request.user),
        'is_owner': info['bids'][0]['user'] == request.user.username,
        })

    # note to self: cannot change the url here
    return render(request, "auctions/listing.html", {
        'listing': info,
        'watched': is_watched(l, request.user),
        'is_owner': info['bids'][0]['user'] == request.user.username,
    })

def create_listing(request):
    return render(request, "auctions/create_listing.html")

def listing_to_info_dict(l):
    info = {
        'title': l.title,
        'description': l.description,
        'image_url': l.image_url,
        'category': l.category,
        'bids': [],
        'comments': [],
        'id': l.id,
    }

    bids = Bid.objects.filter(listing=l)

    for b in bids:
        info['bids'].append({
            'timestamp': b.timestamp.strftime("%m/%d/%Y %H:%M:%S"),
            'price': "$" + str(b.price),
            'user': b.user.username
        })

    comments = Comment.objects.filter(listing=l)
    print(comments)

    for c in comments:
        info['comments'].append({
            'timestamp': c.timestamp.strftime("%m/%d/%Y %H:%M:%S"),
            'message': c.comment,
            'user': c.user.username,
        })


    info['starting_bid'] = info['bids'][0]
    info['current_bid'] = info['bids'][-1]
    return info

def index(request):
    all_listings = []
    for l in Listing.objects.all():
        if (l.is_active == False):
            continue

        info = listing_to_info_dict(l)
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

            # ctg = Category(
            #     category = request.POST["category"],
            #     listing = l
            # )
            # ctg.save()
            # print(ctg)

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