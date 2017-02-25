from django.conf.urls import url
from main import views

app_name = 'main'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^test', views.test, name = 'test'),
	url(r'^index', views.index, name='index'),
	url(r'^register', views.register, name='register'),
	url(r'^login', views.login, name='login'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^rulebook', views.rulebook, name='rulebook'),
	url(r'^display_question', views.display_question, name = 'display_question'),
]