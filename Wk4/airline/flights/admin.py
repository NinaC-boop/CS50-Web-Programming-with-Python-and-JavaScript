from django.contrib import admin

# Register your models here.
# do after migrate
from .models import Flight, Airport, Passenger

class FlightAdmin(admin.ModelAdmin):
    # extra settings for admin page layout
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    # show many to mnay relatoinships
    filter_horizontal = ("flights",)


admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin) # use these particular settings when viewing interface
admin.site.register(Passenger, PassengerAdmin)