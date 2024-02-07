from datetime import datetime
from django.utils import timezone
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control', 'id': 'floatingInput',
                                   'placeholder': 'name@example.com',
                               }))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control', 'id': 'floatingPassword',
                                   'placeholder': 'Password', 'type': 'Password',
                               }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control', 'id': 'floatingInput',
                                   'placeholder': 'name@example.com',
                               }
                               )
                               )
    email = forms.CharField(label='E-mail',
                            required=False,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control', 'id': 'floatingInput',
                                'placeholder': 'name@example.com',
                            }
                            )
                            )
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control', 'id': 'floatingPassword',
                                    'placeholder': 'Password', 'type': 'Password',
                                }))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control', 'id': 'floatingPassword',
                                    'placeholder': 'Password', 'type': 'Password',
                                }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'placeholder': 'name@example.com',
    }
    ), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'placeholder': 'name@example.com',
    }
    ), required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )


class ProfileUserForms(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'name@example.com',
        }
        )
    )
    email = forms.CharField(
        disabled=True,
        required=False,
        label='E-mail',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'name@example.com',
        }
        ))

    this_year = timezone.now().year
    date_of_bird = forms.DateField(
        label='День рождения',
        widget=forms.SelectDateWidget(
            years=tuple(range(this_year - 100, this_year - 5))
        ))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'date_of_bird', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInput',
                'placeholder': 'name@example.com',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInput',
                'placeholder': 'name@example.com',
            }),

            'photo': forms.ClearableFileInput(attrs={
                'class': 'text-center center-block file-upload'
            }),
        }
