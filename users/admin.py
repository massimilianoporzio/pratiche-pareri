# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

# Crea un'istanza dell'AdminSite personalizzato
from pratiche.admin import custom_admin_site
from users.forms import (
    CustomAuthenticationForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)

from .models import CustomUser

# Annulla la registrazione del modello  Group dall'admin di default
admin.site.unregister(Group)


@admin.register(Group, site=custom_admin_site)
class CustomGroupAdmin(admin.ModelAdmin):
    pass  # Lascia vuoto per usare la configurazione di default


# Per personalizzare l'admin del tuo CustomUser, puoi estendere UserAdmin
@admin.register(CustomUser, site=custom_admin_site)
class CustomUserAdmin(UserAdmin):
    # Usa il form personalizzato per la creazione di nuovi utenti
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # I campi da visualizzare nella lista degli utenti nell'admin
    list_display = (
        "email",
        "first_name",
        "last_name",
        "gender",
        "is_staff",
        "is_active",
    )
    # I campi da usare per la ricerca
    search_fields = ("email", "first_name", "last_name")
    # I filtri laterali
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "gender")

    # Ridefinisci fieldsets usando la funzione di traduzione
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "gender")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Ridefinisci add_fieldsets usando la funzione di traduzione
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password",
                    "password2",
                    "gender",
                    "is_staff",
                    "is_active",
                    "groups",
                ),
            },
        ),
    )

    def changeform_view(self, request, object_id=..., form_url=..., extra_context=...):
        extra_context = extra_context or {}
        extra_context["show_close"] = True
        return super().changeform_view(request, object_id, form_url, extra_context)
