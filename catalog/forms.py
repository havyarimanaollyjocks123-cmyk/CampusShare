from django import forms
from .models import Ressource
import os

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ('titre', 'filiere', 'niveau', 'matiere', 'type_document', 'annee_academique', 'semestre', 'enseignant_nom', 'description', 'fichier')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'annee_academique': forms.TextInput(attrs={'placeholder': 'ex: 2023-2024'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajoute la classe CSS 'form-control' à tous les champs pour le style
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if fichier:
            # Vérification de la taille (max 20 Mo)
            if fichier.size > 20 * 1024 * 1024:
                raise forms.ValidationError("Le fichier ne doit pas dépasser 20 Mo.")
            
            # Vérification de l'extension
            extensions_valides = ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png']
            ext = os.path.splitext(fichier.name)[1].lower()
            if ext not in extensions_valides:
                raise forms.ValidationError("Format non autorisé. Utilisez PDF, DOCX, PPTX, JPG ou PNG.")
        return fichier