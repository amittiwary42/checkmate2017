from .models import User_Profile, Host
from django.shortcuts import redirect
from . import views
import re

def game_start():
	host = Host.objects.get(submit_name = "host")
	host.play_allowed = 1
	host.save()
	print('Game Started')

def login_closed():
	host = Host.objects.get(submit_name = "host")
	host.play_allowed = 0
	host.save()
	print('Login Closed')

def game_over():
	up = User_Profile.objects.all()
	for i in up :
		i.allowed_to_play = 0
		i.save()
	print('Game Over')

def check_data(data):
	nameReg=r'[A-z\s]{3,}'
	emaReg=r'([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)'
	phoReg=r'([0-9]{10})'
	teamReg=r'[\s]'
	if (re.match(teamReg,data['team_name'])) :
		return False
	if not (re.match(emaReg,data['email_1']) and re.match(emaReg, data['email_2'])):
		return False
	if not (re.match(phoReg, str(data['phone_1'])) and re.match(phoReg, str(data['phone_2']))):
		return False
	if not (re.match(nameReg, data['name_1']) and re.match(nameReg, data['name_2'])):
		return False
	else:
		return True
