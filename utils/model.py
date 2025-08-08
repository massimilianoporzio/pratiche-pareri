import uuid

from concurrency.fields import IntegerVersionField
from crum import get_current_user
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Model(models.Model):
    """
    We use this for EVERY DB ENTRY making all models inherit from it.
    """

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
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
    version = IntegerVersionField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

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
