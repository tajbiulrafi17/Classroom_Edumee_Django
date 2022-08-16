from dataclasses import field
from django import forms

from .models import StudyMaterials

class Materialform(forms.ModelForm):
    class Meta:
        model = StudyMaterials
        fields = fields = ['title', 'file_resource']