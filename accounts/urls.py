from django.urls import path
from accounts.views.accounts import custom_login, custom_logout

app_name = 'accounts'
urlpatterns = [
    path("member/login", custom_login, name="login"),
    path('member/logout', custom_logout, name='logout'),
    
]
