from django import forms
from django.contrib.auth import get_user_model

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))

    class Meta:
        model=get_user_model()
        fields=['username','email','first_name','last_name', 'password', 'password2']
        labels= {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'фамилия'
        }

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise(forms.ValidationError("пароли не совпадают"))
            return cd['password']
        
        def clean_email(self):
            cd = self.cleaned_data
            if get_user_model().objects.filter(email==cd['email']).exists():
                raise(forms.ValidationError('Такой email уже существует'))
            return cd['email']

class SendVideoForm(forms.Form):
    link = forms.CharField(label='Ссылка', widget=forms.TextInput(attrs={'class':'form-input'})) 