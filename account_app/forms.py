from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account_app.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", 'full_name']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "full_name", "image", "password", "is_active", "is_admin"]


class ContactUsForm(forms.Form):
    subject = forms.CharField(max_length=50, widget=forms.TextInput({'placeholder': 'subject'}))
    message = forms.CharField(widget=forms.Textarea({'placeholder': 'message'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput({'placeholder': 'Email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput({'placeholder': 'Password'}))


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput({'placeholder': 'username'}))
    email = forms.EmailField(widget=forms.EmailInput({'placeholder': 'email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput({'placeholder': 'password'}))


class OtpForm(forms.Form):
    randcode = forms.CharField(max_length=5, widget=forms.TextInput({'placeholder': 'code'}))


class VerifyEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput({'placeholder': 'email'}))


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput({'placeholder': 'new password'}))
    confirmation_password = forms.CharField(max_length=20,
                                            widget=forms.PasswordInput({'placeholder': 'confirmation password'}))
