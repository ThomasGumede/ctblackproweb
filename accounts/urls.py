from django.urls import path
from accounts.views.accounts import custom_login, custom_logout, register, account_details

app_name = 'accounts'
urlpatterns = [
    path("member/login", custom_login, name="login"),
    path('member/logout', custom_logout, name='logout'),
    path('member/sign-up', register, name='sign-up'),
    path('member/@<username>', account_details, name='user-details'),
]
