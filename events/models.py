import uuid
from decimal import Decimal
from django.db import models
from accounts.models import AbstractCreate
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.db.models.signals import pre_delete, post_save
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from datetime import timedelta
from django.utils.safestring import mark_safe
from accounts.utilities.validators import verify_rsa_phone
from events.utilities.choices import StatusChoices
from events.utilities.file_handlers import handle_event_file_upload

PHONE_REGEX = verify_rsa_phone()

class Event(AbstractCreate):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="events")
    image = models.ImageField(help_text=_("Upload event image."), upload_to=handle_event_file_upload, null=True, blank=True)
    title = models.CharField(help_text=_("Enter title for your event"), max_length=150, unique=True)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    small_description = models.TextField(help_text=_("Small description about your event for search"), null=True, blank=True)
    description = HTMLField()
    
    organiser = models.CharField(max_length=350, help_text=_("Enter organiser's full names or title"))
    start_date = models.DateTimeField(validators = [MinValueValidator(timezone.now(), "Event start date and time. It cannot be in the past")])
    end_date = models.DateTimeField(validators = [MinValueValidator(timezone.now(), "Event end date and time. It cannot be in the past")])
    cost = models.DecimalField(max_digits=1000, decimal_places=2, help_text=_("Enter the overall costs of this event"))
    venue_name = models.CharField(max_length=400, help_text=_("Enter event's venue name"))
    address = models.CharField(max_length=300, help_text=_("Enter event address seperated by comma e.g WaterFall Road 1234, Cape Town, WC, RSA"), null=True, blank=True)
    phone = models.CharField(help_text=_("Enter event's cell/tele phone number"), max_length=15, validators=[PHONE_REGEX])
    email = models.EmailField(blank=True, null=True, help_text=_("Enter event's email address for communications"))
    website = models.URLField(blank=True, null=True, help_text=_("Enter event's website starting with 'https://"))
    map_coordinates  = models.CharField(max_length=300, blank=True, null=True)
    form_link = models.URLField(blank=True, null=True, help_text=_("Enter event's booking form link e.g Google Forms, start with https://"))
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.NOT_APPROVED)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-created']

    def date_time_formatter(self):
        start_local = timezone.localtime(self.start_date)
        end_local = timezone.localtime(self.end_date)
        if start_local.date() == end_local.date():
            return f"{start_local.strftime('%a %d %b %Y')}, {start_local.strftime('%H:%M')} - {end_local.strftime('%H:%M')}"
        else:
            return f"{start_local.strftime('%a %d %b %Y, %H:%M')} - {end_local.strftime('%a %d %b %Y, %H:%M')}"
        
    def sales_days_left(self):
        date = self.end_date - timezone.now()
        if date.days < 0:
            return "0 days"
        if date.days > 1:
            return f"{date.days} days"
        else:
            return f"{date.days} day"

    def __str__(self) -> str:
        return f"{self.title}"
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe(f"<img src={self.image.url} alt={self.title}-image height='60' width='90' />")
        return ""

    def content_safe(self):
        return mark_safe(self.description)
    
    def get_absolute_url(self):
        return reverse("events:event-details", kwargs={"event_slug": self.slug})


class EventContent(AbstractCreate):
    image = models.ImageField(help_text=_("Upload emages images."), upload_to=handle_event_file_upload)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    some_field = models.CharField(max_length=20, blank=True, null=True)

@receiver(pre_delete, sender=Event)
def delete_event_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()

@receiver(pre_delete, sender=EventContent)
def delete_event_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()