from . import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
# from django.urls import reverse_lazy
# from django.contrib.admin.widgets import RelatedFieldWidgetWrapper




class SearchForm(forms.Form):
    query = forms.CharField()

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class BlogCreationForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        exclude = ['user']

class VideoCastCreationForm(forms.ModelForm):
    class Meta:
        model = models.Videocast
        exclude = ['user']

class PodCastCreationForm(forms.ModelForm):
    class Meta:
        model = models.Podcast
        exclude = ['user']
        
class SkillCreationForm(forms.ModelForm):
    class Meta:
        model = models.Skill
        exclude = ['user']

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control mb-3'}),
            'last_name':forms.TextInput(attrs={'class':'form-control mb-3'}),
            'email':forms.EmailInput(attrs={'class':'form-control mb-3', 'readonly':True}),
            'username':forms.TextInput(attrs={'class':'form-control mb-3', 'readonly':True}),    
        }