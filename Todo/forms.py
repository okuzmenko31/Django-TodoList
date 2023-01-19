from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Todo, Category


class Registration(UserCreationForm):
    username = forms.CharField(label='Write here the username that you want',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))
    password1 = forms.CharField(label='Create you password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Repeat your password here', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Repeat your password'}))
    email = forms.EmailField(label='Write here your email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Authentication(AuthenticationForm):
    username = forms.CharField(label='Write here your username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))
    password = forms.CharField(label='Write here your password',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'password', 'type': 'password'}))


class TaskCreation(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class TaskUpdate(forms.ModelForm):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    complete = forms.BooleanField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Todo
        fields = ['title', 'complete', 'description', 'category']


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserResetPassword(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
