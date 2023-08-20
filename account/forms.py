from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # check if user is in database
    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(**cleaned_data)
        if user is None:
            raise ValidationError("There is no matching user in the system")
        cleaned_data["user"] = user
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Type password again")
    email = forms.EmailField(label="Email")
    username = forms.CharField(initial="")

    # check if both password are the same
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password1"] != cleaned_data["password2"]:
            raise ValidationError("Passwords don't match")
        return cleaned_data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
