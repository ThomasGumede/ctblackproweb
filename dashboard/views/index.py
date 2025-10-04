from django.shortcuts import render, redirect
from accounts.models import Account
from home.models import Blog
from events.models import Event

def dashboard(request):
    users = Account.objects.all()
    return render(request, "dashboard/index.html", {"users": users})