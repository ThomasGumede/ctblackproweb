from django.contrib import admin
from memberships.models import MembershipEmail, MembershipFile, MembershipApplication

@admin.register(MembershipFile)
class MembershipFile(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    
@admin.register(MembershipApplication)
class ApplicationAdmin(admin.ModelAdmin):
    pass
