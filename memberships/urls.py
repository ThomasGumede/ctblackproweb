from django.urls import path
from memberships.views.application import join_membership, apply_for_membership, application_submitted, trace_application
from memberships.views.membership import download_membership_form, download_membership_rates, download_files

app_name = "memberships"
urlpatterns = [
    path('membership/join-us', join_membership, name='membership'),
    path('membership/membership-application', apply_for_membership, name='apply-membership'),
    path('membership/membership-application/application=<application_number>', apply_for_membership, name='apply-membership-with-number'),
    path('membership/membership-application/<application_id>', application_submitted, name='application-done'),
    path('membership/trace-application', trace_application, name='trace-application'),
    
    path('membership/download-file/<file_slug>', download_files, name='download-files'),
    path('membership/membership-rates', download_membership_rates, name='download-membership-rates'),
    path('membership/membership-form', download_membership_form, name='download-membership-form'),
]
