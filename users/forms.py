from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from temp.models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user', )

        widgets = {'image':forms.FileInput(
         attrs={'required': False}
        )}


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': '','email': ''}
