from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Per personalizzare l'admin del tuo CustomUser, puoi estendere UserAdmin
class CustomUserAdmin(UserAdmin):
    # I campi da visualizzare nella lista degli utenti nell'admin
    list_display = ('email', 'first_name', 'last_name', 'gender', 'is_staff', 'is_active')
    # I campi da usare per la ricerca
    search_fields = ('email', 'first_name', 'last_name')
    # I filtri laterali
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'gender')

    # Aggiungi il campo 'gender' ai fieldsets per la modifica/visualizzazione
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gender',)}),
    )
    # Aggiungi il campo 'gender' ai add_fieldsets per la creazione di nuovi utenti
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('gender',)}),
    )
    
    
    def changeform_view(self, request, object_id = ..., form_url = ..., extra_context = ...):
        extra_context = extra_context or {}
        extra_context['show_close'] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

admin.site.register(CustomUser, CustomUserAdmin)