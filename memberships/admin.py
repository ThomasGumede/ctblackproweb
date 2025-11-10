from django.contrib import admin
from memberships.models import MembershipEmail, MembershipFile, MembershipApplication

@admin.register(MembershipFile)
class MembershipFile(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    

@admin.register(MembershipApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "application_number", "membership_choice", "status", "date_submitted")
    list_filter = ("status", "date_submitted", "membership_choice")
    search_fields = ("application_number", "first_name", "last_name", "email")
    ordering = ("-date_submitted",)
    readonly_fields = ("application_number", "date_submitted")
