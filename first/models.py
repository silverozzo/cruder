from django.contrib.auth.models import AbstractBaseUser, Group
from django.db                  import models

import datetime
import simple_audit

from .managers import CustomUserManager


class Organization(models.Model):
	"""
	Model of organization which can hold a set of users
	"""
	class Meta:
		app_label   = 'first'
		permissions = (
			('view_organization', 'Can view organization'),
		)
	
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
	Custom user model on email authentication identifier.
	Each user can be linked to organization.
	"""
	email = models.EmailField(
		verbose_name = 'email address',
		max_length   = 255,
		unique       = True
	)
	is_active    = models.BooleanField(default=True)
	is_admin     = models.BooleanField(default=False)
	is_staff     = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	groups       = models.ManyToManyField(Group)
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
		print('user permission called')
		return True
	
	def has_module_perms(self, app_label):
		return True


class Teammate(models.Model):
	"""
	Model of guys just for holding in DB.
	"""
	class Meta:
		app_label = 'first'
	
	fullname = models.CharField(max_length=200, default='', blank=True)
	team     = models.ForeignKey(Team)
	
	def __str__(self):
		return self.fullname + ' (' + str(self.team) + ')'


simple_audit.register(Organization)
simple_audit.register(Team)
simple_audit.register(Teammate)
simple_audit.register(CustomUser)
