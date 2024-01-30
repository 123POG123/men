from captcha.fields import CaptchaField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.deconstruct import deconstructible
from django import forms

from .models import Men, Category, Tags


@deconstructible
class RussianValidate():
    ALLOWED_CHARS = 'абвгдеёжзиклмнопрстуфхчщьыъэюя' \
                    'АБВГДЕЁЖЗИКЛМНОПРСТУФХЧЩЬЫЪЭЮЯ' \
                    '0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if self.message else \
            'Должны присутствовать только русские буквы, дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class MenForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 50, 'rows': 5}), required=False, label='Биография'
    )
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': "text-center center-block file-upload image_load"}), label='Изображение',
        required=False
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Таг')

    class Meta:
        model = Men
        fields = ['title', 'cat', 'description', 'image', 'tag', 'data_of_bird']

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'абвгдеёжзиклмнопрстуфхчщьыъэюяАБВГДЕЁЖЗИКЛМНОПРСТУФХЧЩЬЫЪЭЮЯ0123456789- '
        code = 'russian'
        message = 'Должны присутствовать только русские буквы, дефис и пробел !!!!!'
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError(message, code=code)
        return title


class SendUserEmailForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'name': 'nombre',
            'id': 'nombre',
        }
    ), required=False, label='Имя')
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
                'name': 'email',
                'type': 'email',
                'id': 'nombre',
            }))

    comments = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'cols': 50,
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Сообщение',
        }))
    captcha = CaptchaField()
