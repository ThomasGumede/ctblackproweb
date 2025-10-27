# events/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Event, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def image_preview(self, obj):
        """Display image thumbnail in admin"""
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"

    def is_open(self, obj):
        return obj.is_open
    is_open.boolean = True
    is_open.short_description = "Open for Booking"
    
    list_display = (
        "title", 
        "venue_name", 
        "start_date", 
        "end_date", 
        "slots", 
        "available_slots", 
        "is_open", 
        "status",
        "image_preview",
    )
    list_filter = ("status", "start_date", "closing_date")
    search_fields = ("title", "venue_name", "organiser", "address")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("image_preview", "created", "updated")
    date_hierarchy = "start_date"
    ordering = ("-start_date",)
    
    fieldsets = (
        ("📌 Basic Information", {
            "fields": (
                "title", 
                "slug", 
                "author", 
                "organiser",
                "status",
            )
        }),
        ("🖼️ Media", {
            "fields": (
                "image", 
                "image_preview", 
                "small_description", 
                "description"
            )
        }),
        ("📍 Venue & Contact Details", {
            "fields": (
                "venue_name",
                "address",
                "phone",
                "email",
                "website",
                "map_coordinates",
            )
        }),
        ("📅 Event Schedule", {
            "fields": (
                "start_date",
                "end_date",
                "closing_date",
                "cost",
                
                "slots",
            )
        }),
        ("👕 Dress Code", {
            "fields": (
                "dress_code_cap",
                "dress_code_top",
                "dress_code_pants",
            )
        }),
        ("💳 Payment", {
            "fields": (
                "admin_fee",
                "payment_required",
            )
        }),
        ("🔗 Links & Forms", {
            "fields": (
                "form_link",
            )
        }),
        ("🕒 Metadata", {
            "fields": ("created", "updated"),
            "classes": ("collapse",),
        }),
    )

    


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "payment_status", "created", "payment_referrence")
    list_filter = ("payment_status", "created")
    search_fields = ("user__username", "user__first_name", "event__title", "payment_referrence")
    autocomplete_fields = ("event", "user")
    readonly_fields = ("created",)
