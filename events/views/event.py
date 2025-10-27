from events.models import Event
from django.shortcuts import render, get_object_or_404

def events(request):
    events = Event.objects.all()
    
    return render(request, 'events/events.html', {"events": events})

def event_details(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    levents = Event.objects.all().exclude(id=event.id)[:5]
    return render(request, 'events/event-details.html', {"event": event, "levents": levents})