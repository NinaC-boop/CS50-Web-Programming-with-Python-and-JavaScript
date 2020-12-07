from django.db import models




# Create your models here.
# each model is a table
class Airport(models.Model):
    code = models.CharField(max_length=3)

    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    # reference another table
    # what happens to flights when references gets delete. if cascade, if airport, its also gonna delete on flights. models.protect to save
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") # can go backwards if u have flight, how to go backwards from airport to flight
    # origin = models.CharField(max_length=64) # can dinf doc
    # destination = models.CharField(max_length=64)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"










        # all python object returns string reporensentation
    # 1. instruction about how to manipulate
    # 2. tell them to actually use on database

    # python3 manage.py makemigrations
    # create migration in 00001_initial = isntructions how to change database
    # python3 manage.py migrate
    # how to actually apply
    # enter python shell -> python3 manage.py shell
#     >>> from flights.models import Flight
# >>> f = Flight(origin="NewYork", destination = "London", duration = 4235)
# >>> f.save
# <bound method Model.save of <Flight: Flight object (None)>>
# # >>> f.save()
# Flight.objects.all() show all
# flight = flights.first() <- first row
# flight.id flight.origin, flight.delete()