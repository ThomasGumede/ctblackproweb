from home.views.home import index, about, contact, gallery, club_documents
from django.urls import path

app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('about-us', about, name='about'),
    path('about-us/gallery', gallery, name='gallery'),
    path('about-us/club-documents', club_documents, name='club-documents'),
    path('contact-us', contact, name='contact'),
]
