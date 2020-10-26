from django.urls import path

from . import views

app_name = "wiki"
# note: always put <str:title> at the end or else it'll cover all results
urlpatterns = [
    path("", views.index, name="index"),
    path("search_results", views.search_view, name="search"),
    path("new", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.rand, name="random"),
    path("<str:title>", views.page, name="page"),
]
