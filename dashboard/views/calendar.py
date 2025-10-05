from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import JsonResponse
from accounts.models import Account
from home.models import Blog
from events.models import Event

def index(request):
    events = Event.objects.all().order_by('created')
    return render(request, "dashboard/calendar/index.html", {"events": events})

def get_events(request):
    events = Event.objects.all()
    data = serializers.serialize("json", events)
    return JsonResponse({"success": True, "events": data}, status=200)
    