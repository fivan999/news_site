from django import forms
from .models import *
import re
from PIL import Image
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


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


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control mb-4'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control mb-4'}))
    password2 = forms.CharField(label='Подтвердите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control mb-4'}))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control mb-4'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control mb-4'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control mb-4'}))


class MailSendForm(forms.Form):
    subject = forms.CharField(label='Тема',
                              widget=forms.TextInput(attrs={'class': 'form-control mb-4'}))
    text = forms.CharField(label='Текст',
                           widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': 5}))
    receivers = forms.CharField(label='Получатели (через пробел)',
                                widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': 5}))
