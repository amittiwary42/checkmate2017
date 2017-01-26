from django.contrib.auth.models import User
from django import forms
from .models import *

class Team_Form(forms.Form):
	team_name = forms.CharField(max_length = 50,label = 'Team Name:')
	password = forms.CharField(widget = forms.PasswordInput(), max_length = 50)
	name_1 = forms.CharField(max_length = 50,label = 'Name of 1st Participant:')
	idno_1 = forms.CharField(max_length = 12)
	phone_1 = forms.IntegerField(widget = forms.TextInput(), min_value = 6000000000, label = 'Phone No. of 1st Participant:')
	email_1 = forms.EmailField(label = 'Email of 1st Participant:')
	name_2 = forms.CharField(max_length = 50, required = False, label = 'Name of 2nd Participant:')
	idno_2 = forms.CharField(max_length = 12)
	phone_2 = forms.IntegerField(widget = forms.TextInput(), required = False, min_value = 6000000000, label = 'Phone of 2nd Participant:')
	email_2 = forms.EmailField(required = False, label = 'Email of 2nd Participant:')

class Login_Form(forms.Form):
	team_name = forms.CharField(max_length = 50)
	password = forms.CharField(widget = forms.PasswordInput())