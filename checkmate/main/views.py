from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User_Profile, Host
from .forms import Team_Form, Login_Form
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
import json

# For all views: status : 0 => Some probem, status : 1 => No problem
def index(request):
	# Return a rendered response to send to the client.
	return render(request, 'main/index.html')

# View for Registration
def register(request):
	if request.user.is_authenticated:
		retrun redirect('/main/')
	
	else:
		if form.method == 'POST':
			form = Team_Form(request.POST)
			
			if form.is_valid():
				data = form.cleaned_data
				
				if not check_data(data): # check_data function to be made!!
					resp = { 
						'status':0,
						'error_message':'Form fields are not correct!! Please enter them properly.'
					}
					return HttpResponse(json.dumps(resp), content_type = "application/json")
				
				u = User()
				u.username = data['team_name']
				u.set_password = data['password']
				
				try:
					u.save()
				
				except IntegrityError:
					resp = {
						'status':0,
						'message':'Team Name already exists!! Please choose a different Team Name'
					}
					return HttpResponse(json.dumps(resp), content_type = "application/json")

				# Creating User Profile
				up = User_Profile()
				up.user = u
				up.team_name = data['team_name']
				up.name_1 = data['name_1']
				up.idno_1 = data['idno_1']
				up.phone_1 = data['phone_1']
				up.email_1 = data['email_1']
				up.name_2 = data['name_2']
				up.idno_2 = data['idno_2']
				up.phone_2 = data['phone_2']
				up.email_2 = data['email_2']
				up.save()

				resp = {
					'status':1,
					'message':'Successfully Registered', 
					'teamname' : up.team_name
				}
				return HttpResponse(json.dumps(resp), content_type = "application/json")
			
			else:
				resp = { 
					'status':0,
					'error_message':'Form fields are not correct. Enter them properly.'
				}
				return HttpResponse(json.dumps(resp), content_typeif = "application/json")

		else :
			form = Team_Form()
			return render(request, 'main/register.html', {'form' : form})

# View for Login
def login(request):
	if request.user.is_authenticated:
		return redirect(request, '/main/')
	
	else:
		if request.method == 'POST':
			form = Login_Form(request.POST)
			
			if form.is_valid():
				data = form.cleaned_data
				team_name = data['team_name']
				password = data['password']
				user = authenticate(username = team_name, password = password)
				
				try:
					up = User_Profile.objects.get(user = user)
					host = Host.objects.get(host_name = "host")
					
					if host.play_allowed == 0:
						resp = {
							'status':0,
							'error_message':'Game has not started yet!! Stay tuned to change the FUTURE!!'
						}
						return HttpResponse(json.dumps(resp), content_type = 'application/json')
					
					if up.allowed_to_play == 0:
						resp = {
							'status':0,
							'error_message':'Game has ended. Thanks for playing'
						}
						return HttpResponse(json.dumps(resp), content_type = 'application/json')

				except:
					resp = {
						'status':0,
						'error_message':'Team Name or Password is incorrect!! Please try again.'
					}
					return HttpResponse(json.dumps(resp), content_type = 'application/json')

				if user is not None:
					if user.is_active:
						login(request, user)
						resp = {
							'status':1,
							'message':'Login Successful'
						}
						return HttpResponse(json.dumps(resp), content_type = 'application/json')

					else:
						resp = {
							'status':0,
							'error_message':'Your account is inactive. Contact the site administrator'
						}
						return HttpResponse(json.dumps(resp), content_type = 'application/json')

				else:
					resp = {
						'status':0,
						'error_message':'Your Team Name or Password was incorrect!! Please try again.'
					}
					return HttpResponse(json.dumps(resp), content_type = 'application/json')

			else:
				resp = {
					'status':0,
					'error_message':'Your form credentials are not valid!! Please try again.'
				}
				return HttpResponse(json.dumps(resp), content_type = 'application/json')

		else:
			form = Login_Form()
			return redirect(request, 'main/register.html', {'form':form})
