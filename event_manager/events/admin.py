from django.contrib import admin
from events.models import Event, Venue


admin.site.register(Event)
admin.site.register(Venue)
