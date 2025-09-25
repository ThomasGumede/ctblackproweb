from django.urls import path
from accounts.views.accounts import custom_login, custom_logout
from accounts.views.club import get_club_files, download_file
from accounts.views.member import membership

app_name = 'accounts'
urlpatterns = [
    path("member/login", custom_login, name="login"),
    path('member/logout', custom_logout, name='logout'),
    path('member/club-documents', get_club_files, name='documents'),
    path('member/club-document/<file_id>', download_file, name='download-file'),
    path('member/join-us', membership, name='membership'),
]
