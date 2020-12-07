from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    # sencond arg is the function name
    path("logout", views.logout_view, name="logout"),
]