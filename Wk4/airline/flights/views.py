from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all() # get all flights
    })

def flight(request, flight_id):
    #use pk or id. pk is primary key
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        # exclude not filter
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        # add a new row to a table
        passenger.flights.add(flight)
        # gets name of view e.g. name=flight_name and reverses to gives url ()path
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))


#     >>> Airport.objects.filter(city="New York")
# <QuerySet [<Airport: New York (JFK)>]>

# first and only one
# >>> Airport.objects.filter(city="New York").first()
# <Airport: New York (JFK)>
# >>> Airport.objects.get(city="New York")
# <Airport: New York (JFK)>