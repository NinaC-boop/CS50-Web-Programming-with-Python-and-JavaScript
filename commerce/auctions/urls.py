from django.urls import path

from . import views

urlpatterns = [
    # goes to path, returns view which takes in arguments and returns a html page
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("make_bid", views.make_bid, name="make_bid"),
    path("closed_listing", views.close_auction, name="close_auction"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:ctg>", views.category, name="category"),
]
