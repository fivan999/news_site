from django import forms
from .models import *
import re
from PIL import Image
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-4'}),
            'content': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': 5}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input mb-1'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select md-4'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
