from django.contrib import admin
from accounts.models import Account, Company

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(Company)
class AboutClubAdmin(admin.ModelAdmin):
    pass
