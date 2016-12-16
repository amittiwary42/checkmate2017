from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	# Return a rendered response to send to the client.
	return render(request, 'main/index.html')