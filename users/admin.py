# Register your models here.
from django.contrib import admin

from pratiche.admin import CustomAdminSite

from .models import CustomUser

# Crea un'istanza dell'AdminSite personalizzato
custom_admin_site = CustomAdminSite(name="custom_admin")
