from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import User_Profile, Host, Question, City
from .forms import Team_Form, Login_Form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .controls import *
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect

# For all views: status : 0 => Some probem, status : 1 => No problem
def test(request):
	return HttpResponse('Is this working?')

def index(request):
	if not request.user.is_authenticated():
		return redirect('/main/register/')
	else :
		up = User_Profile.objects.get(user = request.user)
		if up.allowed_to_play == 0:
			resp = {
				'status' : 0,
				'message' : "Time's up"

			}
			return HttpResponse(json.dumps(resp), content_type = "application/json")
		else:
			#send attempted questions and correct questions
			
			return render(request, 'main/index.html')

# View for Registration
@csrf_exempt
def register(request):
	if request.user.is_authenticated():
		return redirect('/main/login/')
	else:
		if request.method == 'POST':
			form = Team_Form(request.POST)

			if form.is_valid():
				data = form.cleaned_data

				if not check_data(data):
					resp = {
						'status':0,
						'message':'Form fields are not correct!! Please enter them properly.'
					}
					return HttpResponse(json.dumps(resp), content_type = "application/json")
				
				if(data['password'] != data['confirm_password']):
					resp = {
						'status':0,
						'message':'Password fields do not match. Re-enter password.'
					}
					return HttpResponse(json.dumps(resp), content_type = "application/json")
				# print(data['password'])
				u = User.objects.create_user(
					username = data['team_name'],
					password = data['password'],
					email = data['email_1']
				)
				try:
					u.save()
					print(u.has_usable_password())
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
					'message':'Form fields are not correct. Enter them properly.'
				}
				return HttpResponse(json.dumps(resp), content_type = "application/json")

		else :
			form = Team_Form()
			return render(request, 'main/register.html', {'form' : form})

# View for Login
@csrf_exempt
def login(request):
	if request.user.is_authenticated():
		return redirect('/main/')

	else:
		if request.method == 'POST':
			form = Login_Form(request.POST)

			if form.is_valid():
				print('form is valid')
				data = form.cleaned_data
				team_name = data['team_name']
				password = data['password']
				print(team_name)
				user = authenticate(username = team_name, password = password)

				try:
					print("entered try")
					up = User_Profile.objects.get(user = user)
					print("got up")
					host = Host.objects.get(host_name = "host")
					print("authenticated")
					print(up)
					print(host)
					if host.play_allowed == 0:
						resp = {
							'status':0,
							'message':'Game has not started yet!! Stay tuned!!'
						}
						return HttpResponse(json.dumps(resp), content_type = 'application/json')

					if up.allowed_to_play == 0:
						resp = {
							'status':0,
							'message':'Game has ended. Thanks for playing'
						}
						return HttpResponse(json.dumps(resp), content_type = 'application/json')

				except:
					resp = {
						'status':0,
						'message':'Team Name or Password is incorrect!! Please try again.'
					}
					return HttpResponse(json.dumps(resp), content_type = 'application/json')

				if user is not None:
					if user.is_active:
						auth_login(request, user)
						# resp = {
							# 'status':1,
							# 'message':'Login Successful'
						# }
						# return HttpResponse(json.dumps(resp), content_type = 'application/json')
						return redirect('/main/index/')
					else:
						resp = {
							'status':0,
							'message':'Your account is inactive. Contact the site administrator'
						}
						return HttpResponse(json.dumps(resp), content_type = 'application/json')

				else:
					resp = {
						'status':0,
						'message':'Your Team Name or Password was incorrect!! Please try again.'
					}
					return HttpResponse(json.dumps(resp), content_type = 'application/json')

			else:
				resp = {
					'status':0,
					'message':'Your form credentials are not valid!! Please try again.'
				}
				return HttpResponse(json.dumps(resp), content_type = 'application/json')

		else:
			form = Login_Form()
			return render(request, 'main/register.html', {'form':form})

# View for rulebook
def rulebook(request):
	return render(request, 'main/rulebook.html')

#View for logging out
@login_required
def logout(request):
	logout(request)
	return redirect('/main/login.html')

@login_required
@csrf_exempt
def display_question(request):
	user = request.user
	up = User_Profile.objects.get(user = user)

	if up.allowed_to_play == 0 :
		resp = {
			'status' : 0,
			'message' : "Time's up"
		}
		return HttpResponse(json.dumps(resp), content_type = "application/json")


	if request.POST:
		if str(request.POST.get('no')).isdigit():
			number = int(request.POST.get('no'))
		else:
			print("from point1")
			raise Http404
	else:
		raise Http404
	print(number)
	try:
		question = Question.objects.get(question_no = number)
		city = City.objects.get(question_no = number)
	except:
		print("from point2")
		raise Http404

	trial = (int(number) - 1)
	aq = up.attempted_questions.split()
	cq = up.correct_questions.split()

	if aq[trial] == '3' :
		resp = {
			'status' : 0,
			'message' : 'You cannot attempt this question anymore.'
		}
		return HttpResponse(json.dumps(resp), content_type = "application/json")

	elif cq[trial] == '1':
		resp = {
			'status' : 0,
			'message' : 'You cannot attempt this question anymore.'
		}
		return HttpResponse(json.dumps(resp), content_type = "application/json")

	#aq[trial] = str(int(aq[trial])+1)
	#up.attempted_questions = ' '.join(aq)
	resp = {
		'status': 1,
		'question' : str(question.content),
		'visited' : aq[trial]
	}

	up.save()

	return HttpResponse(json.dumps(resp), content_type = "application/json")

#View for the main game logic
@login_required
@csrf_exempt
def answer(request):
	print("Entered Answer")
	user = request.user
	up = User_Profile.objects.get(user = user)
	if up.allowed_to_play == 0:
		resp = {
			'status' : 0,
			'message' : "Time's up"
		}
		return HttpResponse(json.dumps(resp), content_type = "application/json")
	if request.POST:
		number = int(request.POST.get('no'))
		answer = str(request.POST.get('ans'))
		print("answer")
		print(request.POST)
		question = get_object_or_404(Question, question_no = number)
		trial = (int(number)-1)
		aq = up.attempted_questions.split()
		cq = up.correct_questions.split()
		if aq[trial] == '3' or cq[trial] == '1' :
			raise Http404
		answer = answer.lower()
		if answer == question.answer:
			cq[trial] = '1'
			up.correct_questions = ' '.join(cq)
			if question.difficulty_level == 1:
				if aq[trial] == '0':
					up.population += 30000
				elif aq[trial] == '1':
					up.population += 25000
				elif aq[trial] == '2':
					up.population += 20000
			if question.difficulty_level == 2:
				if aq[trial] == '0':
					up.population += 30000
				elif aq[trial] == '1':
					up.population += 25000
				elif aq[trial] == '2':
					up.population += 20000
			if question.difficulty_level == 3:
				if aq[trial] == '0':
					up.population += 30000
				elif aq[trial] == '1':
					up.population += 25000
				elif aq[trial] == '2':
					up.population += 20000
			up.save()
			#why print? (ref:pokemon checkmate)
			resp = {
				'status' : 1,
				'population' : up.population,
				#do we need to send visited and correct?
			}
			return HttpResponse(json.dumps(resp), content_type = "application/json")

		else:
			aq[trial] = str(int(aq[trial])+1)
			up.attempted_questions = ' '.join(aq)
			up.save()
			resp = {
				'status' : 0,
				'population' : up.population
			}
			return HttpResponse(json.dumps(resp), content_type = "application/json")
	else:
		resp = {
			'status' : 1
		}
		return HttpResponse(json.dumps(resp), content_type = "application/json")
