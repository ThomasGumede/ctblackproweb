from events.views.event import event_details, events
from django.urls import path

app_name = "events"
urlpatterns = [
    path('events', events, name='events'),
    path('event/<event_slug>', event_details, name='event-details'),
]


# Create your views here.
