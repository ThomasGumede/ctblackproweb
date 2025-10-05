from django.db import models
from accounts.models import AbstractCreate
from memberships.utilities.handle_file import handle_file_upload
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

MFILE_TITLES = (
    ("Membership Joining Form", "Membership Joining Form"),
    ("Membership Rates", "Membership Rates"),
    ("Other", "Other"),

)

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