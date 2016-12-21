from django.db import models

# Create your models here.

class info(models.Model):
	
	name = models.CharField(max_length=20)
	email = models.CharField(max_length=100)
	mobile = models.CharField(max_length=10)
	age = models.CharField(max_length=3)
	dob = models.CharField(max_length=100)
	location = models.CharField(max_length=100)

	def __str__(self):
		return self.name