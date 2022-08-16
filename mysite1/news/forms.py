from django import forms
from .models import *


class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Название новости', widget=forms.TextInput(attrs={'class': 'form-control mb-4'}))
    content = forms.CharField(label='Контент новости', required=False, widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': 5}))
    is_published = forms.BooleanField(label='Опубликовать', required=False, initial=True,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-check-input mb-1'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберите категорию', widget=forms.Select(attrs={'class': 'form-select md-4'}))
