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
]
