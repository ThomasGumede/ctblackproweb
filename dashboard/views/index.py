from django.shortcuts import render, redirect
from accounts.models import Account
from events.models import Event, Booking
from memberships.models import MembershipApplication
from django.contrib.auth.decorators import login_required

def dashboard(request):
    users = Account.objects.filter(is_active=True)
    inusers = Account.objects.filter(is_active=False)
    bookings = MembershipApplication.objects.all()
    events = Event.objects.all()
    
    context = {
        "users": users,
        "inusers": inusers,
        "events": events,
    }
    return render(request, "dashboard/index.html", context)