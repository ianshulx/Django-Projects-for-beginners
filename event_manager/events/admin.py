from django.contrib import admin
from events.models import Event, Venue, Ticket, EventReview


admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(EventReview)
admin.site.register(Ticket)