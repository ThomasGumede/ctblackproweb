from django.contrib import admin
from memberships.models import MembershipEmail, MembershipFile

@admin.register(MembershipFile)
class MembershipFile(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
