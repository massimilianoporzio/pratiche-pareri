from django.db import models

from utils.model import Model as MyModel


# Create your models here.
class TipoOrigine(MyModel):
    """
    Model representing the origin type of a document.
    """

    nome = models.CharField(max_length=50, verbose_name="nome dell'ente", unique=True)

    class Meta:
        verbose_name = "Ente inviante"
        verbose_name_plural = "Enti invianti"

    def __str__(self):
        return self.nome
