from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import EmailValidator


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[EmailValidator])
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def clean_password2(self) -> str:
        return super().clean_password2()

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.set_password(self.clean_password2())
        setattr(user, 'first_name', self.cleaned_data['first_name'])
        setattr(user, 'last_name', self.cleaned_data['last_name'])
        setattr(user, 'email', self.cleaned_data['email'])
        if commit:
            user.save()
        return user
