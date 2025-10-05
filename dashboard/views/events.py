from django.shortcuts import render, redirect
from events.models import Event

def events(request):
    events = Event.objects.all()
    return render(request, "dashboard/events/index.html", {"events": events})