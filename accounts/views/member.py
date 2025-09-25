from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

def membership(request):
    return render(request, 'membership/join-us.html')