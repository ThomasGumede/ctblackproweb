from django.contrib import admin
from memberships.models import MembershipEmail, MembershipFile, MembershipApplication

@admin.register(MembershipFile)
class MembershipFile(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    
@admin.register(MembershipApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant_names", "application_number", "status", "date_submitted")
    list_filter = ("status", "date_submitted")
    search_fields = ("application_number", "user__username", "user__first_name",)
    ordering = ("-date_submitted",)
    readonly_fields = ("user", "application_number")
