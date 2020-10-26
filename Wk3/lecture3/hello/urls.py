from django.urls import path
from . import views

urlpatterns = [ 
    # all accessible urls, uses path
    path("", views.index, name="index"), 
    # first url. no additional argument > what view when visited > give name to URL
    path("nina", views.nina, name="nina"),
    path("johnson", views.johnson, name="johnson"),
    path("<str:name>", views.greet, name="greet") 
    # any string, put into a variable called "name"
]