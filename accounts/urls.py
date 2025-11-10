from django.urls import path
from accounts.views.accounts import custom_login, custom_logout, register, account_details
from accounts.views.password import password_reset_request, password_reset_sent, passwordResetConfirm, password_change
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

app_name = 'accounts'
urlpatterns = [
    path("member/login", custom_login, name="login"),
    path('member/logout', custom_logout, name='logout'),
    path('member/sign-up', register, name='sign-up'),
    path('member/@<username>', account_details, name='user-details'),
    path("password/reset", password_reset_request, name="password-reset"),
    path('password/success', password_reset_sent, name='password-reset-sent'),
    path("password/reset", password_reset_request, name="password-reset"),
    path('password/success', password_reset_sent, name='password-reset-sent'),
    path('password/reset/<uidb64>/<token>', passwordResetConfirm, name='password-reset-confirm'),
]
