from home.views.home import index, about, contact
from django.urls import path

app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('about-us', about, name='about'),
    path('contact-us', contact, name='contact'),
]
