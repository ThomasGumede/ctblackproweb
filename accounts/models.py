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
# from memberships.models import MemberAppChoices

PHONE_VALIDATOR = verify_rsa_phone()

PROVINCES = [
    ("kzn", "KwaZulu-Natal"),
    ("mp", "Mpumalanga"),
    ("nw", "North-West"),
    ("fs", "Free-State"),
    ("wc", "Western Cape"),
    ("lp", "Limpopo"),
    ("gp", "Gauteng"),
    ("ec", "Eastern Cape"),
    ("nc", "Northern Cape"),
]

ROLE_CHOICES = [
        ("Chairman", "Chairman"),
        ("Public Relations Officer", "Public Relations Officer"),
        ("Captain", "Captain"),
        ("Vice Captain", "Vice Captain"),
        ("Treasurer", "Treasurer"),
        ("Secretary", "Secretary"),
        ("Chairman Rules and Discipline", "Chairman: Rules and Discipline Committee"),
        ("Member", "General Member")
    ]

RACE_CHOICES = [
        ("African", "African"),
        ("Coloured", "Coloured"),
        ("Indian", "Indian"),
        ("White", "White"),
        ("Other", "Other"),
    ]


GENDER_CHOICES = [
        ("Male", "Male"),  # only male allowed
    ]


class AbstractProfile(models.Model):
    """Reusable contact and social media fields."""
    address = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(
        help_text=_("Enter cellphone number"),
        max_length=15,
        validators=[PHONE_VALIDATOR],
        unique=True,
        null=True,
        blank=True,
    )
    facebook = models.URLField(validators=[validate_fcbk_link], blank=True, null=True)
    twitter = models.URLField(validators=[validate_twitter_link], blank=True, null=True)
    instagram = models.URLField(validators=[validate_insta_link], blank=True, null=True)
    linkedIn = models.URLField(validators=[validate_in_link], blank=True, null=True)

    class Meta:
        abstract = True


class AbstractCreate(models.Model):
    """Base model that adds UUID and timestamps."""
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        editable=False,
        db_index=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(AbstractUser, AbstractProfile):
    """Custom user model for club members."""
    profile_image = models.ImageField(
        help_text=_("Upload profile image"),
        upload_to=handle_profile_upload,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=30, choices=TITLE_CHOICES, default=TITLE_CHOICES[0])
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="Male",
        help_text=_("Male Only Club"),
    )
    race = models.CharField(max_length=50, choices=RACE_CHOICES)
    membership_number = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True)
    hna_membership_number = models.CharField(max_length=50, blank=True, null=True)
    biography = models.TextField(
        blank=True,
        help_text=_("Tell us a little bit about your professional or business."),
    )
    is_technical = models.BooleanField(default=False)
    is_email_activated = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ["-created"]

    def __str__(self):
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse("accounts:user-details", kwargs={"username": self.username})

    def get_full_user_address(self):
        return self.address or _("No address provided")
    

    @property
    def is_approved(self):
        """
        Returns True if user’s application has been approved.
        """
        return hasattr(self, "membership_application") and self.membership_application.status == "APPROVED"
    
    

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
   
    def __str__(self):
        return self.title
    
    class Meta: 
        verbose_name = 'About Company'
        verbose_name_plural = 'About Companys'
        
    