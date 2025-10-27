# bookings/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "billing_name", "billing_surname", "billing_email",
            "billing_phone", "billing_address", "company_name",
            "company_address", "booking_note", "payment_method",
        ]
        widgets = {
            "booking_note": forms.Textarea(attrs={"rows": 3}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }
        
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''
