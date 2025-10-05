from django.urls import path
from dashboard.views.index import dashboard
from dashboard.views.users import accounts, user, delete_user, profile, update_profile, update_profile_password
from dashboard.views.events import events
from dashboard.views.documents import documents
from dashboard.views.company import company
from dashboard.views.calendar import index, get_events

app_name = "dashboard"

urlpatterns = [
    path("dashboard", dashboard, name="dashboard"),
    
    path("dashboard/members", accounts, name="users"),
    path("dashboard/members/@<username>", user, name="user-details"),
    path("dashboard/members/delete/@<username>", delete_user, name="delete-user"),
    
    path("dashboard/profile/@<username>", profile, name="profile-details"),
    path("dashboard/profile-update/@<username>", update_profile, name="profile-update"),
    path("dashboard/profile/password/@<username>", update_profile_password, name="profile-update-password"),
    
    path("dashboard/events", events, name="events"),
    path("dashboard/documents", documents, name="documents"),
    
    path("dashboard/company", company, name="company"),
    
    path("dashboard/calendar", index, name="calendar"),
    path("dashboard/api/get-events", get_events, name="get-events-api"),
]
