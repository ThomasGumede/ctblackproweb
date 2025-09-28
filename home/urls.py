from home.views.home import index, about, contact, gallery, club_documents
from home.views.club_files import get_club_files, download_file
from django.urls import path

app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('about-us', about, name='about'),
    path('about-us/gallery', gallery, name='gallery'),
    path('about-us/club-documents', get_club_files, name='documents'),
    path('about-us/club-document/<file_id>', download_file, name='download-file'),
    path('contact-us', contact, name='contact'),
]
