# Create your models here.
from concurrency.fields import IntegerVersionField
from crum import get_current_user
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


# Manager personalizzato per il tuo CustomUser
class CustomUserManager(BaseUserManager):
    def full_clean(self, email):
        if not email.endswith("@aslcn1.it"):
            raise ValidationError(
                _("Il dominio dell'indirizzo email deve essere 'aslcn1.it'.")
            )

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("L'indirizzo email deve essere impostato"))
        # Aggiungi la validazione qui
        self.full_clean(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Aggiungi la validazione qui
        self.full_clean(email)
        # Imposta i campi necessari per un superuser
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault(
            "is_active", True
        )  # I superuser dovrebbero essere attivi per default

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser deve avere is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser deve avere is_superuser=True."))

        # Chiama il metodo create_user del manager, passando l'email
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # Rimuovi il campo username se vuoi usare solo l'email per l'autenticazione
    # Non è necessario rimuoverlo esplicitamente, ma puoi renderlo non obbligatorio
    # o semplicemente non usarlo.
    # Se vuoi che l'email sia l'UNICO campo per l'autenticazione, devi impostare:
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Campi richiesti oltre a USERNAME_FIELD e password

    email = models.EmailField(_("indirizzo email aziendale"), unique=True)
    username = models.CharField(
        _("nome utente"), max_length=150, unique=True, blank=True, null=True
    )
    GENDER_CHOICES = [
        ("M", "Maschio"),
        ("F", "Femmina"),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,  # Rendi il campo facoltativo
        null=True,  # Permetti valori NULL nel database
        verbose_name=_("genere"),
    )

    # Aggiungi qui eventuali altri campi personalizzati
    version = IntegerVersionField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_%(class)s_set",
    )
    created_by_fullname = models.CharField(max_length=150, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_%(class)s_set",
    )
    updated_by_fullname = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.get_full_name()

    # Assegna il manager personalizzato al tuo modello utente
    objects = CustomUserManager()

    @property
    def email_prefix_display(self):
        """Restituisce la parte dell'email prima della @ per la visualizzazione."""
        if self.email:
            return self.email.split("@")[0]
        return ""

    def get_short_name(self):
        """Restituisce il prefisso dell'email come nome breve."""
        return self.email_prefix_display

    @property
    def nome_utente(self):
        """Restituisce il nome completo dell'utente."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.get_short_name()

    def clean(self):
        super().clean()
        if self.email and not self.email.endswith("@aslcn1.it"):
            raise ValidationError(
                _("Il dominio dell'indirizzo email deve essere 'aslcn1.it'.")
            )

    def save(self, *args, **kwargs):

        if not self.username and self.email:
            self.username = self.email_prefix_display
        user = get_current_user()
        if user and not user.is_anonymous:
            # Se il record è nuovo (non ha ancora una chiave primaria)
            if not self.pk:
                self.created_by = user
                self.created_by_fullname = (
                    user.nome_utente if hasattr(user, "nome_utente") else str(user)
                )
            # L'utente che ha fatto l'ultima modifica è sempre l'utente corrente
            self.updated_by = user
            self.updated_by_fullname = (
                user.nome_utente if hasattr(user, "nome_utente") else str(user)
            )

        super().save(*args, **kwargs)
