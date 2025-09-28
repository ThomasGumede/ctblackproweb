from django.urls import path

from memberships.views.membership import join_membership, download_membership_form, download_membership_rates

app_name = "memberships"
urlpatterns = [
    path('membership/join-us', join_membership, name='membership'),
    path('membership/membership-rates', download_membership_rates, name='download-membership-rates'),
    path('membership/membership-form', download_membership_form, name='download-membership-form'),
]
