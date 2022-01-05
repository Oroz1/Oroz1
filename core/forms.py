from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import *
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=155,
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class RegistretionForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistretionForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'})
    class Meta:
        model = NewUser
        fields = ('name', 'username', 'phone_number', 'password1', 'password2')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Фамилия и имя', 'required': ''}),
            'username': forms.TextInput(attrs={'placeholder': 'Придумайте имя пользователя'}),
            'phone_number': forms.NumberInput(attrs={'placeholder': 'Номер телефона'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('subject', 'group')

        widgets = {
          'subject': forms.CheckboxSelectMultiple(attrs={}),
          'group': forms.CheckboxSelectMultiple(attrs={}),
        }


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['group'].empty_label = 'Выберите свой класс'
    class Meta:
        model = Student
        fields = ['group']
