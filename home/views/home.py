import logging
from django.shortcuts import render, redirect
from events.models import Event
from django.contrib import messages
from home.models import Media,  Member
from home.forms import EmailForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

from home.utilities.custom_email import send_email_to_admin

logger = logging.getLogger("tasks")


def index(request):
    events = Event.objects.all()[:3]
    images = Media.objects.all()[:3]
    
    return render(request, 'home/index.html', {"events": events, "images": images})

def about(request):
    members = Member.objects.all()
    return render(request, 'home/about-us.html', {"members": members})

def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recaptcha_token = form.cleaned_data.get('recaptcha_token')
            # print(recaptcha_token)
            try:
                
                form.save()
                send_email_to_admin(form.cleaned_data["subject"], form.cleaned_data["message"], form.cleaned_data["from_email"], form.cleaned_data["name"])
                messages.success(request, "We have successfully receive your email, will be in touch shortly")
                return redirect("home:contact")
            
            except ValueError as e:
                logger.error(f"Failed to verify this due to f{e}")
                messages.success(request, "We have successfully receive your email, will be in touch shortly")
                return redirect("home:contact")
            
            
        else:
            messages.error(request, "Something went wrong, please fix errors below")
            for err in form.errors:
                messages.error(request, f"{err}")
                return redirect("home:contact")
            
    form = EmailForm()
    return render(request, "home/contact-us.html", {"form": form})

def gallery(request):
    images = Media.objects.all()
    return render(request, 'home/gallery.html', {"images": images})

def club_documents(request):
    return render(request, 'home/documents.html')