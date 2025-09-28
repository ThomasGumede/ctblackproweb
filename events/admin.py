from django.contrib import admin
from events.models import Event, EventContent

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}

@admin.register(EventContent)
class EventContent(admin.ModelAdmin):
    pass