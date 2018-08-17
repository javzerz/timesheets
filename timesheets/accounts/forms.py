from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.forms.widgets import PasswordInput, TextInput, SelectDateWidget, Textarea
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from .models import UserProfile, Timecard
from django.forms import ModelForm

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    email = forms.EmailField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Email'}),max_length=75)
    email_confirm = forms.EmailField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Confirm Email'}),max_length=75, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'email_confirm', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(self.cleaned_data['password'])
        return password

    def clean_email_confirm(self):
        print(self.cleaned_data)
        email = self.cleaned_data.get('email')
        email_confirm = self.cleaned_data.get('email_confirm')
        if email != email_confirm:
            raise forms.ValidationError("Whops!.. XD.. emails must match")

        email_exists = User.objects.filter(email=email)
        if email_exists.exists():
            raise forms.ValidationError("Whops! This email already exists")

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password',}))

class EditProfileForm(UserChangeForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    email = forms.EmailField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Email'}),max_length=75)

    class Meta:
        model = User
        fields = {'username','email', 'password'}

class UpdateProfileForm(ModelForm):
    bio = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Bio'}),max_length=500)
    department = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Department'}),max_length=500)
    position = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Position'}),max_length=500)
    phone = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Phone'}),max_length=20)

    class Meta:
        model = UserProfile
        fields = {'bio', 'department', 'position','phone'}

class TimecardForm(forms.ModelForm):

    YEAR_CHOICES = ('2015', '2016', '2017', '2018', '2019')

    project = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Project'}),max_length=500)
    hours = forms.IntegerField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Hours'}))
    date = forms.DateField(widget=SelectDateWidget(attrs={'class':'form-control','placeholder': 'Date'},years=YEAR_CHOICES))
    comments = forms.CharField(widget=Textarea(attrs={'class':'form-control','placeholder': 'Comments','rows':2}),max_length=500)

    class Meta:
        model = Timecard
        fields = {'project','date','hours','comments'}
