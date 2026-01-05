from django import forms

class SendLinkForm(forms.Form):
    link = forms.CharField(label = 'Ссылка',widget=forms.TextInput(attrs={'class':'form-input'}))

class CreateCompanyForm(forms.Form):
    name = forms.CharField(label = 'Имя', widget=forms.TextInput(attrs={'class':'form-input'}))
    description = forms.CharField(label = 'Описание', widget=forms.TextInput(attrs={'class':'form-input'}))