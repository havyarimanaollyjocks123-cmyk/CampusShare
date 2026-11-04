from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'filiere', 'niveau')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter la classe CSS 'form-control' à tous les champs automatiquement
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ConnexionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'