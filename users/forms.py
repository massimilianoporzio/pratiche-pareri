from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(
        label=_("Password"), strip=False, widget=forms.PasswordInput
    )

    def __init__(self, request=None, *args, **kwargs):
        """
        Salva la request e passa gli altri argomenti al costruttore del form padre.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not username:
            raise ValidationError(_("L'indirizzo email non può essere vuoto."))

        # PRIMO STEP: Validazione del formato e del dominio dell'email
        try:
            # Verifica il formato dell'email
            validate_email(username)
        except ValidationError:
            raise ValidationError(
                _("Per favore, inserisci un indirizzo email valido come username.")
            )

        # Verifica il dominio
        if not username.endswith("@aslcn1.it"):
            raise ValidationError(
                _("Il dominio dell'indirizzo email deve essere 'aslcn1.it'.")
            )

        # SECONDO STEP: Autenticazione (solo se la validazione del formato e del dominio passano)
        if password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise ValidationError(
                    _(
                        "Inserisci un indirizzo email aziendale e password corretti per un account di staff."
                    )
                )
        else:
            raise ValidationError(_("La password non può essere vuota."))

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


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
