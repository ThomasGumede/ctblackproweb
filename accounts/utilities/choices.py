from django.db import models

TITLE_CHOICES = (
    ("Mr", "Mr"),
    ("Mrs", "Mrs"),
    ("Ms", "Ms"),
    ("Dr", "Dr"),
    ("Prof", "Prof.")
)

class IdentityNumberChoices(models.TextChoices):
    ID_NUMBER = ("ID_NUMBER", "ID number")
    PASSPORT = ("PASSPORT", "Passport")

class Gender(models.TextChoices):
    MALE = ("MALE", "Male")
    FEMALE = ("FEMALE", "Female")
    OTHER = ("OTHER", "Other")
