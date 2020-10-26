from django.urls import path
from . import views

app_name = "tasks" # give all urls an appname... avoid namespace collision
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add")
    #when i go to the add route, i want to go views.add function and call the function add
]