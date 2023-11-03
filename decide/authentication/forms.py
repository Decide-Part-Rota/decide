# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 
from django.core.validators import RegexValidator
from .models import Person
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField

sex=[("woman","Woman"),("man","Man"),("other","Other")]
status=[("single","Single"),("partner","Partner"),("married","Married"),("divorced","Divorced"),("widow","Widow")]
discord_validator = RegexValidator('.+#\d{4}')

class PersonForm(UserCreationForm):
    sex = forms.ChoiceField(choices=sex, required=True, label="Select your gender")
    age = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=status, required=True, label="Seleccione su estado civil")
    discord_account = forms.CharField(required=False, help_text="Please use the following format: name#XXXX", validators=[discord_validator], max_length=30)
    country = CountryField().formfield()

    def clean_age(self):
        data = self.cleaned_data["age"]

        if not data:
          self.add_error("age", "Debes especificar una edad")

        if data == 0:
          self.add_error("age", "Introduce una edad valida")
        return data
    
    
    
    class Meta:
          model=User
          fields=["username","password1","password2","email","sex","age","status","country","discord_account"]


class CompleteForm(forms.Form):
    sex = forms.ChoiceField(choices=sex, required=True)
    age = forms.IntegerField(required=True)
    status = forms.ChoiceField(choices=status, required=True, label="Select your civil status")
    country = CountryField().formfield()
    discord_account = forms.CharField(required=False, help_text="Please use the following format: name#XXXX", validators=[discord_validator], max_length=30)





# No se usa
class LoginForm(forms.Form):
     username = forms.CharField(label='Usuario',widget=forms.TextInput,required=True)
     password = forms.CharField(label='Contraseña',widget=forms.PasswordInput,required=True)




'''
def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       return self.cleaned_data
'''