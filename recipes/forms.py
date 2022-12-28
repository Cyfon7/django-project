from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'class': "form-control text-center", 'placeholder': "Username"}))
    email = forms.EmailField(label="", required=True, widget=forms.EmailInput(attrs={'class': "form-control text-center", 'placeholder': "Email"}))
    password1 = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={'class': "form-control text-center", 'placeholder': "Password"}))
    password2 = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={'class': "form-control text-center", 'placeholder': "Password Confirmation"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
