from django import forms#DjangoForm
from AccountApp.models import *



class uyelik_Tipi_Form(forms.ModelForm):
    class Meta :
        model = uyelik
        fields = ['uyelikTipi']

class girisForm(forms.Form):
    kullanici = forms.CharField(max_length=30,label='',widget=forms.TextInput(attrs={'placeholder': 'Kullanıcı Adınızı Giriniz :'}))
    sifre = forms.CharField(max_length=30,label='',widget=forms.PasswordInput(attrs={'placeholder': 'Şifrenizi Giriniz:'}))


