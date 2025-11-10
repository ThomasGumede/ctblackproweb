from django import forms
from memberships.models import MembershipApplication, MembershipEmail, MembershipFile, MembershipRates
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
    membership_choice = forms.ChoiceField(
        choices=MembershipRates.choices,
        widget=forms.Select(attrs={"class": "selectize"}),
        label="Membership Choice"
    )

    class Meta:
        model = MembershipApplication  # <-- updated to use the standalone application model
        fields = [
            "title",
            "profile_image",
            "first_name",
            "last_name",
            "gender",
            "biography",
            "race",
            "address",
            "email",
            "phone",
            "linkedIn",
            "hna_membership_number",
            "membership_choice",  # include here
        ]

        widgets = {
            'profile_image': forms.FileInput(attrs={
                "class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"
            }),
            'title': forms.Select(attrs={"class": "selectize"}),
            'first_name': forms.TextInput(attrs={
                "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"
            }),
            'last_name': forms.TextInput(attrs={
                "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"
            }),
            'gender': forms.Select(attrs={"class": "selectize"}),
            'race': forms.Select(attrs={"class": "selectize"}),
            'membership_choice': forms.Select(attrs={"class": "selectize"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'
            if self.initial.get(field_name) is None:
                self.initial[field_name] = ''

                
    # def save(self, commit=True):
    #     user = super().save(commit)
    #     membership_choice = self.cleaned_data.get("membership_choice")
    #     MembershipApplication.objects.update_or_create(
    #         user=user,
    #         defaults={"membership_choice": membership_choice}
    #     )
    #     return user
