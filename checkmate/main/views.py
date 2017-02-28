from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import User_Profile, Host, Question, City
from .forms import Team_Form, Login_Form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
from django.contrib.auth.decorators import login_required

# For all views: status : 0 => Some probem, status : 1 => No problem
def test(request):
	return HttpResponse('Is this working?')

def index(request):
	if not request.user.is_authenticated() :
		return render(request, 'main/register.html')
	else :
		up = UserProfile.objects.get(user = request.user)
		if up.allowed_to_play == 0:
			resp = {
				'status' : 0,
				'error_message' : "Time's up"
			}
			return HttpResponse(json.dumps(resp), content_type = "application/json")

		else:
			return render(request, 'main/register.html')

# View for Registration
def register(request):
	if request.user.is_authenticated:
		return redirect('/main/')

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
		return redirect('/main/')

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
def display_question(request):
	user = request.user
	up = UserProfile.objects.get(user = user)

	if up.allowed_to_play == 0 :
		resp = {
			'status' : 0,
			'error_message' : "Time's up"
		}
		return HttpResponse(json.dumps(resp), content_type = "application/json")


	if request.POST :
		if str(request.POST.get('num')).isdigit():
			number = int(request.POST.get('num'))
		else:
			raise Http404
	else:
		raise Http404

	try:
		question = Question.objects.get(question_no = number)
		city = City.objects.get(question_no = number)
	except:
		raise Http404

	trial = (int(number) - 1)
	aq = up.attempted_questions.split()
	cq = up.correct_questions.split()

	if aq[trial] == '3' :
		resp = {
			'status' : 0,
			'error_message' : 'You cannot attempt this question anymore.'
		}
		return HttpResponse(json.dumps(resp), content_type = "application/json")

	elif cq[trial] == '1':
		resp = {
			'status' : 0,
			'error_message' : 'You cannot attempt this question anymore.'
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
	def answer(request):
		user = request.user
		up = UserProfile.objects.get(user = user)
		if up.allowed_to_play == 0:
			resp = {
				'status' : 0,
				'error_message' : "Time's up"
			}
			return HttpResponse(json.dumps(resp), content_type = "application/json")
		if request.POST:
			number = int(request.POST.get('num'))
			answer = str(request.POST.get('answer'))
			question = get_object_or_404(Question, number = number)
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
