from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class User_Profile(models.Model):
	user = models.OneToOneField(User) #extending user model
	team_name = models.CharField(max_length = 50)
	name_1 = models.CharField(max_length = 50)
	idno_1 = models.CharField(max_length = 12)
	phone_1 = models.BigIntegerField(null = True)
	email_1 = models.EmailField()
	name_2 = models.CharField(max_length = 50, blank = True)	
	idno_2 = models.CharField(max_length = 12, blank = True)
	phone_2 = models.BigIntegerField(blank = True, null = True)
	email_2 = models.EmailField(blank = True, null = True)
	attempted_questions = models.CharField(max_length = 39, default = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0")
	# List of questions attempted [0-Not Attempted, 1-Attempted once, 2-Attempted Twice, 3-Attempted Thrice/Blocked]
	correct_questions = models.CharField(max_length = 39, default = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0")
	# List of correctly attempted questions [0-Attempted Wrongly, 1-Attempted Correctly, 2-On Question]
	allowed_to_play = models.IntegerField(default = 0)
	# If allowed to play - 1 else 0
	
	def __str__(self):
		return self.user.username

class Host(models.Model):
	host_name = models.CharField(max_length = 10, default = "host")
	play_allowed = models.IntegerField(default = 0)

	def __str__(self):
		return self.host_name