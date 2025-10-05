from django.shortcuts import render, redirect
from accounts.models import Account
from home.models import Blog
from events.models import Event

def dashboard(request):
    users = Account.objects.filter(is_active=True)
    inusers = Account.objects.filter(is_active=False)
    events = Event.objects.all()
    
    context = {
        "users": users,
        "inusers": inusers,
        "events": events,
    }
    return render(request, "dashboard/index.html", context)