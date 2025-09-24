from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about-us.html')

def contact(request):
    return render(request, 'home/contact-us.html')