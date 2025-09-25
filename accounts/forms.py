from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (AuthenticationForm,  UserCreationForm)

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'id': 'id_username'}), label="Username or Email*")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'id_password'}))

class RegistrationForm(UserCreationForm):
    confirm_email = forms.EmailField(help_text="Confirm your email address", required=True, widget=forms.EmailInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'email': forms.EmailInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'confirm_email': forms.EmailInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'first_name': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'last_name': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            #'hobbies': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'password1': forms.PasswordInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'password2': forms.PasswordInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(f'This email: {email} is already in use.')
        
        return email
    
    def clean(self):
        clean = super().clean()
        second_email = clean.get("confirm_email", None)
        mail = clean.get("email", None)

        if second_email and mail and mail != second_email:
            raise forms.ValidationError(f'This email: {mail} does not match with confirmation email.')
        
        

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user