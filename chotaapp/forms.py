from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from chotaapp.models import Customer



class signupform(UserCreationForm):
    class Meta:
        model=User

        fields=['username','first_name','last_name','email']
        labels={'email':'Email'}

class CustomeProfileform(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','email','address','district','state','pincode']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'email':forms.TextInput(attrs={'class':'form-control'}),
                 'address':forms.TextInput(attrs={'class':'form-control'}),
                 'district':forms.TextInput(attrs={'class':'form-control'}),
                 'state':forms.TextInput(attrs={'class':'form-control'}),
                 'pincode':forms.NumberInput(attrs={'class':'form-control'})}


   
        
        