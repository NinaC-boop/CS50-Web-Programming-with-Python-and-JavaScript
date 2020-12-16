from django.http import HttpResponse # django documentation
from django.shortcuts import render

# Create your views here.
# each function is something the user wants to see (view)
# request represents HTTP request (object)
def index(request):
    return render(request, "hello/index.html")


def nina(request):
    return HttpResponse("Hello, Nina")


def johnson(request):
    return HttpResponse("Hello, Johnson!")


# url -> views -> greet
def greet(request, name):
    return render(request, "hello/greet.html", {
        # CONTEXT represented by python dictionary
        # all the variables i want it to have
        "name": name.capitalize()
    })
    # gets request > renders html template > passes name from urls.py into a dictionary

#    def greet(request, name):
#    return HttpResponse(f"Hello, {name.capitalize()}")