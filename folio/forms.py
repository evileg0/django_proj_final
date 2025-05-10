from django import forms
from .models import Folio

class FolioForm(forms.ModelForm):
    class Meta:
        model = Folio
        fields = ['name', 'description']
        labels = {
            'name': 'Название портфеля',
            'description': 'Описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }