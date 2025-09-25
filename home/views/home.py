from django.shortcuts import render
from events.models import Event
from home.models import Media, Blog, BlogCategory

def index(request):
    events = Event.objects.all()[:3]
    images = Media.objects.all()[:3]
    posts = Blog.objects.all()[:3]
    return render(request, 'home/index.html', {"events": events, "images": images})

def about(request):
    return render(request, 'home/about-us.html')

def contact(request):
    if request.method == 'POST':
        pass
    return render(request, 'home/contact-us.html')

def gallery(request):
    images = Media.objects.all()
    return render(request, 'home/gallery.html', {"images": images})

def club_documents(request):
    return render(request, 'home/documents.html')