import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from accounts.utilities.choices import TITLE_CHOICES
from accounts.utilities.file_handlers import handle_profile_upload
from accounts.utilities.validators import validate_fcbk_link, validate_in_link, validate_insta_link, validate_twitter_link, verify_rsa_phone

PHONE_VALIDATOR = verify_rsa_phone()

class Account(AbstractUser):
    profile_image = models.ImageField(help_text=_("Upload profile image"), upload_to=handle_profile_upload, null=True, blank=True)
    title = models.CharField(max_length=30, choices=TITLE_CHOICES, default=TITLE_CHOICES[0])
    maiden_name = models.CharField(help_text=_("Enter your maiden name"), max_length=300, blank=True, null=True)
    biography = models.TextField(blank=True)
    is_technical = models.BooleanField(default=False)
    is_email_activated = models.BooleanField(default=False)
    membership_start_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ["-created"]

    def get_full_user_address(self):
        return f"{self.address_one}, {self.city}, {self.province}, {self.zipcode}"
    
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if self.title:
            return f"{self.title} {self.first_name[0]} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"
        
    def get_absolute_url(self):
        return reverse("accounts:user-details", kwargs={"username": self.username})

class AbstractCreate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Company(AbstractCreate):
    title = models.CharField(max_length=300, null=True, blank=True, unique=True)
    slogan = models.CharField(max_length=300, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=300, default="about-ct-black-pro", unique=True)
    operating_hours = models.CharField(max_length=300, null=True, blank=True, unique=True)
    address = models.CharField(max_length=300, null=True, blank=True, unique=True, help_text="Add club main address e.g Central park, KZN, 7441")
    address_coordinates = models.CharField(max_length=300, null=True, blank=True, help_text="Add club main address coordinates separated by comma e.g 10.00,12.66")
    number_of_members = models.IntegerField(default=0)
    number_of_golf_holes = models.IntegerField(default=0)
    number_of_golf_areas = models.IntegerField(default=0)
    phone = models.CharField(help_text=_("Enter telephone number"), max_length=15, validators=[PHONE_VALIDATOR], unique=True, null=True, blank=True)
    alternate_phone = models.CharField(help_text=_("Enter other telephone number"), max_length=15, validators=[PHONE_VALIDATOR], unique=True, null=True, blank=True)
    facebook = models.URLField(validators=[validate_fcbk_link], blank=True, null=True, help_text=_("Enter facebook link e.g https://www.facebook.com/profile"))
    twitter = models.URLField(validators=[validate_twitter_link], blank=True, null=True, help_text=_("Enter twitter link e.g https://www.twitter.com/profile"))
    instagram = models.URLField(validators=[validate_insta_link], blank=True, null=True, help_text=_("Enter instagram link e.g https://www.instagram.com/profile"))
    linkedIn = models.URLField(validators=[validate_in_link], blank=True, null=True, help_text=_("Enter linkedin link e.g https://www.linkedin.com/profile"))
    email = models.EmailField(null=True, blank=True)
    small_description = models.TextField(null=True, blank=True)
    vision = models.TextField(blank=True, null=True, unique=True)
    mission = models.TextField(blank=True, null=True, unique=True)
    club_profile = models.FileField(help_text=_("Upload club profile"), upload_to=handle_profile_upload, null=True, blank=True)
    club_membership_rates = models.FileField(help_text=_("Upload club membership rates"), upload_to=handle_profile_upload, null=True, blank=True)
    club_membership_form = models.FileField(help_text=_("Upload club membership joining form"), upload_to=handle_profile_upload, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'About Company'
        verbose_name_plural = 'About Companys'
        
class ClubFile(AbstractCreate):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField(help_text=_("Write a short description about this media file"), max_length=200)
    mediafile = models.FileField(help_text=_("Upload club file."), upload_to=handle_profile_upload)
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=None, related_name="club_files", null=True)
    
    def __str__(self):
        return self.title
    