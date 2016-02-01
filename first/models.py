from django.contrib.auth.models import AbstractBaseUser 
from django.db                  import models

import datetime
import simple_audit

from .managers import CustomUserManager


class Foobar(models.Model):
	"""
	Model of foobar entity just for tests and something else.
	"""
	class Meta:
		app_label = 'first'
	
	content_text = models.CharField(max_length=200)
	counter      = models.IntegerField(default=0)
	extra_file   = models.FileField(upload_to='uploads/', blank=True)
	
	def __str__(self):
		return self.content_text + '(' + str(self.id) + ')'


class Organization(models.Model):
	"""
	Model of organization which can hold a set of users
	"""
	class Meta:
		app_label = 'first'
	
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name


class Team(models.Model):
	class Meta:
		app_label = 'first'
	
	name         = models.CharField(max_length=200)
	organization = models.ForeignKey(Organization)
	
	def __str__(self):
		return self.name


class CustomUser(AbstractBaseUser):
	"""
	User model on email authentication identifier
	Each user can be linked to organization
	"""
	email = models.EmailField(
		verbose_name = 'email address',
		max_length   = 255,
		unique       = True
	)
	is_active    = models.BooleanField(default=True)
	is_admin     = models.BooleanField(default=False)
	organization = models.ForeignKey(Organization, blank=True, default=None, null=True)
	
	objects = CustomUserManager()
	
	USERNAME_FIELD  = 'email'
	REQUIRED_FILEDS = []
	
	def __str__(self):
		return self.email
	
	def get_full_name(self):
		return self.email
	
	def get_short_name(self):
		return self.email
	
	def has_perm(self, perm, obj=None):
		return True
	
	def has_module_perms(self, app_label):
		return True
	
	@property
	def is_staff(self):
		return self.is_admin


class Teammate(models.Model):
	"""
	Model of many-to-many link between user and team
	"""
	class Meta:
		app_label = 'first'
	
	user = models.ForeignKey(CustomUser)
	team = models.ForeignKey(Team)
	
	def __str__(self):
		return str(self.team) + ': ' + str(self.user)


simple_audit.register(Foobar)
simple_audit.register(Organization)
simple_audit.register(Team)
simple_audit.register(Teammate)
simple_audit.register(CustomUser)
