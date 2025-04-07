from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        # Verificar si ya existe un usuario con el mismo nombre, apellido y email
        if first_name and last_name and email:
            if User.objects.filter(first_name=first_name, last_name=last_name, email=email).exists():
                raise forms.ValidationError(
                    "Ya existe un usuario registrado con el mismo Nombre, Apellido y Correo electrónico."
                )

        return cleaned_data