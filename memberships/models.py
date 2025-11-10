from django.db import models
from accounts.models import GENDER_CHOICES, RACE_CHOICES, AbstractCreate, AbstractProfile
from accounts.utilities.choices import TITLE_CHOICES
from accounts.utilities.file_handlers import handle_profile_upload
from memberships.utilities.handle_file import handle_file_upload
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

MFILE_TITLES = (
    ("Membership Joining Form", "Membership Joining Form"),
    ("Membership Rates", "Membership Rates"),
    ("Other", "Other"),

)

class MembershipRates(models.TextChoices):
    CPT = "CPT", "Cape Town Membership (R4500)"
    COUNTRY = "COUNTRY", "Country Membership (R2250)"
    ESWATINI = "ESWATINI", "Eswatini Membership (R1200.00)"

class MemberAppChoices(models.TextChoices):
    NOT_APPROVED = "NOT_APPROVED", "Not approved"
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    COMPLETED = "COMPLETED", "Awaiting Payment"
    BLOCKED = "BLOCKED", "Blocked"


class MembershipApplication(AbstractCreate, AbstractProfile):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, db_index=True)
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
    payment_id = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True)
    hna_membership_number = models.CharField(max_length=50, blank=True, null=True)
    biography = models.TextField(
        blank=True,
        help_text=_("Tell us a little bit about your professional or business."),
    )
    application_number = models.CharField(max_length=250, unique=True, db_index=True)
    membership_choice = models.CharField(
        max_length=50,
        choices=MembershipRates.choices,
        default=MembershipRates.CPT,
        help_text="Choose Membership choice as seen on membership rates page"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Cost of membership based on membership choice")
    )
    status = models.CharField(
        max_length=50,
        choices=MemberAppChoices.choices,
        default=MemberAppChoices.NOT_APPROVED,
        help_text="Application status"
    )
    date_submitted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_submitted"]

    def __str__(self):
        return f"Application from {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.title + '. ' if self.title else ''}{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Auto-set cost based on membership choice
        membership_costs = {
            MembershipRates.CPT: 4500.00,
            MembershipRates.COUNTRY: 2250.00,
            MembershipRates.ESWATINI: 1200.00,
        }
        if not self.cost:
            self.cost = membership_costs.get(self.membership_choice, 0)
        super().save(*args, **kwargs)

class MembershipFile(AbstractCreate):
    title = models.CharField(max_length=250, unique=True, help_text=_("Choose a title for this file"), choices=MFILE_TITLES)
    slug = models.SlugField(max_length=300, unique=True, db_index=True)
    file = models.FileField(help_text=_("Upload membership file e.g Membership Joining Form or Membership Rates"), upload_to=handle_file_upload)
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=None, related_name="membership_files", null=True, help_text=_("Select the author of this file e.g Your account"))
    
    class Meta:
        verbose_name = 'Membership File'
        verbose_name_plural = 'Membership Files'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(MembershipFile, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("memberships:download-files", kwargs={"file_slug": self.slug})

class MembershipEmail(AbstractCreate):
    from_email = models.EmailField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    task_id = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Membership Email'
        verbose_name_plural = 'Membership Emails'
        ordering = ["created"]

    def __str__(self) -> str:
        return self.from_email