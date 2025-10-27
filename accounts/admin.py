from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    def profile_image_tag(self, obj):
        """Display user profile image thumbnail in admin."""
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.profile_image.url)
        return _("No Image")

    profile_image_tag.short_description = "Profile Image"

    # Columns in list view
    list_display = (
        "username", "email", "first_name", "last_name", 
        "phone", "gender", "race", "role", "is_staff", "created", "profile_image_tag"
    )
    list_filter = ("gender", "race", "role", "is_staff", "is_superuser", "created")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    ordering = ("-created",)
    readonly_fields = ("created", "updated", "profile_image_tag")

    # Add password entry field to add form
    # add_fieldsets = (
    #     (None, {
    #         "classes": ("wide",),
    #         "fields": (
    #             "username",
    #             "password1",
    #             "password2",
    #             "first_name",
    #             "last_name",
    #             "email",
    #             "phone",
    #             "gender",
    #             "race",
    #             "title",
    #             "hna_membership_number",
    #             "biography",
    #             "profile_image",
    #             "address",
    #             "facebook",
    #             "twitter",
    #             "instagram",
    #             "linkedIn",
    #             "role",
    #             "is_staff",
    #             "is_superuser",
    #         ),
    #     }),
    # )
    add_fieldsets = (
        ("Personal Info", {
            "fields": (
                "username",
                "first_name",
                "last_name",
                "email",
                "title",
                "gender",
                "race",
                "profile_image_tag",
                "profile_image",
                "password1",
                "password2",
                
            ),
        }),
        ("Club Info", {
            "fields": (
                "hna_membership_number",
                "biography",
                
            ),
        }),
        ("Contact & Socials", {
            "fields": (
                "phone",
                "address",
                "facebook",
                "twitter",
                "instagram",
                "linkedIn",
            ),
        }),
        
        ("Permissions", {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
                "is_technical",
                "is_email_activated",
            ),
        }),
        ("Important Dates", {
            "fields": ("last_login", "created", "updated"),
        }),
    )

    # Edit form layout
    fieldsets = (
        ("Personal Info", {
            "fields": (
                "username",
                
                "first_name",
                "last_name",
                "email",
                "title",
                "gender",
                "race",
                "profile_image_tag",
                "profile_image",
                
            ),
        }),
        ("Contact & Socials", {
            "fields": (
                "phone",
                "address",
                "facebook",
                "twitter",
                "instagram",
                "linkedIn",
            ),
        }),
        ("Club Info", {
            "fields": (
                "hna_membership_number",
                "biography",
                "role",
                "is_technical",
                "is_email_activated",
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important Dates", {
            "fields": ("last_login", "created", "updated"),
        }),
    )

    
