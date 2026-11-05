from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'filiere', 'niveau')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On ajoute la classe CSS et on limite la taille de tous les champs
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            # On limite la saisie à 150 caractères max par sécurité
            field.widget.attrs['maxlength'] = '150'

        # On applique une limite plus stricte sur les mots de passe (ex: 50 caractères)
        self.fields['password1'].widget.attrs['maxlength'] = '50'
        self.fields['password2'].widget.attrs['maxlength'] = '50'


class ConnexionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['maxlength'] = '150' # Sécurité pour la connexion