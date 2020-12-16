from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

# tasks = []

class NewTaskForm(forms.Form): # inherits from forms.Form > add all the inputs you want the user to provide
    task = forms.CharField(label="New Task") # name
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = [] # if there's no tasks variable
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })
# python manage.py migrate -> creates all the default tables for data

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST) # create form by using all the data, and filling form
        if form.is_valid(): # validation
            task = form.cleaned_data["task"] # all the data that was submitted
            # tasks.append(task)
            request.session["tasks"] += [task] # append the task
            return HttpResponseRedirect(reverse("tasks:index")) # redirect. reverse engineer index
        else:
            return render(request, "tasks/add.html", {
                "form": form # all errors made
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm() # auto make empty form
    })