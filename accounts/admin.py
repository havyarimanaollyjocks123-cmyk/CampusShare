from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # On ajoute nos champs personnalisés à l'affichage
    fieldsets = UserAdmin.fieldsets + (
        ('Informations CampusShare', {'fields': ('role', 'filiere', 'niveau')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations CampusShare', {'fields': ('role', 'filiere', 'niveau')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'filiere', 'niveau', 'is_staff')
    list_filter = ('role', 'filiere', 'niveau', 'is_staff')
    list_editable = ('role',) 