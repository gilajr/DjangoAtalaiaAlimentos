from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Informe um endereço de email válido', required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este endereço de e-mail já está em uso.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label='Nome de usuário:')
    password = forms.CharField(label='Senha', strip=False, widget=forms.PasswordInput)
    
    error_messages = {
        'invalid_login': (
            "Por favor, insira um nome de usuário e senhas corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas."
        ),
        'inactive': ("Está conta está inativa.")
    }