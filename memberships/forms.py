from django import forms
from memberships.models import MembershipEmail, MembershipFile
from django.contrib.auth import get_user_model

class TraceApplicationForm(forms.Form):
    application_number = forms.CharField(max_length=200)
    email = forms.EmailField()

class MembershipEmailForm(forms.ModelForm):
    recaptcha_token = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = MembershipEmail
        fields = ["from_email", "name", "phone", "message", "recaptcha_token"]
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["title", "profile_image", "first_name", "last_name", 'gender', "biography", "race", "address", "email", "phone", "linkedIn", "hna_membership_number"]

        widgets = {
            'profile_image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'username': forms.TextInput(attrs={"class": "inline-block font-semibold text-neutral-600 dark:text-neutral-200 text-sm mb-2"}),
            'title': forms.Select(attrs={"class": "selectize"}),
            'first_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'gender': forms.Select(attrs={"class": "selectize"}),
            'race': forms.Select(attrs={"class": "selectize"}),
            'last_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            
            
        }

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''