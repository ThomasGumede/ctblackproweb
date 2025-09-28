from django import forms
from memberships.models import MembershipEmail, MembershipFile

class MembershipEmailForm(forms.ModelForm):
    recaptcha_token = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = MembershipEmail
        fields = ["from_email", "name", "phone", "message", "recaptcha_token"]