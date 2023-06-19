from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


#  login form


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid login")
        return super(LoginForm, self).clean()


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password (Again)',
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            "A user with that username already exists."
        )

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords must match.")
        return self.cleaned_data

    def save(self):
        User.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1')
        )
