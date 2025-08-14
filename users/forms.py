from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Ripeti password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "gender",
            "is_staff",
            "is_active",
            "groups",
        )

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Le password non corrispondono.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "gender",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
