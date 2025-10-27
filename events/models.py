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
from django.conf import settings
from django.urls import reverse
from tinymce.models import HTMLField
from datetime import timedelta
from django.utils.safestring import mark_safe
from accounts.utilities.validators import verify_rsa_phone
from events.utilities.choices import StatusChoices
from events.utilities.file_handlers import handle_event_file_upload

PHONE_REGEX = verify_rsa_phone()
# events/models.py
# events/models.py

class Event(AbstractCreate):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="events")
    image = models.ImageField(help_text=_("Upload event image."), upload_to=handle_event_file_upload, null=True, blank=True)
    title = models.CharField(help_text=_("Enter title for your event"), max_length=150, unique=True)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    small_description = models.TextField(help_text=_("Small description about your event for search"), null=True, blank=True)
    description = HTMLField()

    organiser = models.CharField(max_length=350, help_text=_("Enter organiser's full names or title"))
    start_date = models.DateTimeField(validators=[MinValueValidator(timezone.now(), "Event start date and time. It cannot be in the past")])
    end_date = models.DateTimeField(validators=[MinValueValidator(timezone.now(), "Event end date and time. It cannot be in the past")])
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Enter the overall costs of this event"))
    venue_name = models.CharField(max_length=400, help_text=_("Enter event's venue name"))
    address = models.CharField(max_length=300, help_text=_("Enter event address separated by commas e.g. WaterFall Road 1234, Cape Town, WC, RSA"), null=True, blank=True)
    phone = models.CharField(help_text=_("Enter event's cell/tele phone number"), max_length=15, validators=[PHONE_REGEX])
    email = models.EmailField(blank=True, null=True, help_text=_("Enter event's email address for communications"))
    website = models.URLField(blank=True, null=True, help_text=_("Enter event's website starting with 'https://'"))
    map_coordinates = models.CharField(max_length=300, blank=True, null=True)
    form_link = models.URLField(blank=True, null=True, help_text=_("Enter event's booking form link e.g Google Forms, start with https://"))
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.NOT_APPROVED)

    # 🟢 New fields for golf games
    slots = models.PositiveIntegerField(default=4, help_text=_("Number of available player slots"))
    closing_date = models.DateField(help_text=_("Last date to confirm attendance"))
    dress_code_cap = models.CharField(max_length=100, blank=True, null=True)
    dress_code_top = models.CharField(max_length=100, blank=True, null=True)
    dress_code_pants = models.CharField(max_length=100, blank=True, null=True)

    # 🟢 Optional: payment fee fields
    admin_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text=_("Admin costs for payment gateway"))
    payment_required = models.BooleanField(default=True)
    member_discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50.00,
        help_text=_("Member discount in percentage (e.g. 50 for 50%)"),
    )

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def get_discounted_cost(self):
        """Return cost considering membership discount."""
        if self.member_discount:
            discount = (self.member_discount / Decimal(100)) * self.cost
            return round(self.cost + self.admin_fee - discount, 2)
        return self.cost
    
    def get_absolute_url(self):
        return reverse("events:event-details", kwargs={"event_slug": self.slug})

    # 🟢 Booking helpers
    @property
    def is_open(self):
        from django.utils import timezone
        return timezone.now().date() <= self.closing_date and self.available_slots > 0
    
    @property
    def date_time_formatter(self):
        start_local = timezone.localtime(self.start_date)
        end_local = timezone.localtime(self.end_date)
        if start_local.date() == end_local.date():
            return f"{start_local.strftime('%a %d %b %Y')}, {start_local.strftime('%H:%M')} - {end_local.strftime('%H:%M')}"
        else:
            return f"{start_local.strftime('%a %d %b %Y, %H:%M')} - {end_local.strftime('%a %d %b %Y, %H:%M')}"
    
    @property
    def available_slots(self):
        """Return remaining booking slots."""
        confirmed = self.bookings.filter(payment_status="confirmed").count()
        return max(0, self.slots - confirmed)

PAYMENT_METHODS = (
    ("EFT", "EFT"),
    ("Cash on Arrival", "Cash on Arrival"),
    ("Yoco", "Yoco (Unavailable)"),
)

class Booking(AbstractCreate):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")

    # Billing Information
    billing_name = models.CharField(max_length=100)
    billing_surname = models.CharField(max_length=100)
    billing_email = models.EmailField()
    billing_phone = models.CharField(max_length=15)
    billing_address = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    booking_note = models.TextField(blank=True, null=True)

    # Payment Details
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default=PAYMENT_METHODS[0])
    payment_status = models.CharField(max_length=20, choices=StatusChoices, default=StatusChoices.NOT_APPROVED)

    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_referrence = models.CharField(max_length=200, unique=True, db_index=True, editable=False)

    def calculate_total_cost(self):
        """Compute total cost based on event cost + discount."""
        is_member = hasattr(self.user, "membership_application") and getattr(self.user.membership_application, "status", StatusChoices.APPROVED)
        if is_member:
            return self.event.get_discounted_cost()
        else:
            return self.event.admin_fee + self.event.cost

    def save(self, *args, **kwargs):
        """Auto-calculate total cost before saving."""
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)
        
    
    
    def __str__(self):
        return f"{self.user.get_full_name()} — {self.event.title}"

@receiver(pre_delete, sender=Event)
def delete_event_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()
