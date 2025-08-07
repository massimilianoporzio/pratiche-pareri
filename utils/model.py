import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Model(models.Model):
    """
    We use this for EVERY DB ENTRY making all models inherit from it.
    """

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
