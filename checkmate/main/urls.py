from django.conf.urls import url
from main import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index.html', views.index, name='index'),
	url(r'^register.html', views.register, name='register')
	url(r'^login.html', views.login, name='login'),
]