from django.db import models

class StatusChoices(models.TextChoices):
    NOT_APPROVED = ("NOT APPROVED", "Not approved")
    PENDING = ("PENDING", "Pending")
    APPROVED = ("APPROVED", "Approved")
    COMPLETED = ("Completed", "Completed")
    BLOCKED = ("Blocked", "Blocked")