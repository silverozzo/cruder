from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.db                  import models

import datetime
import simple_audit


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


class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('email for users is required')
		
		user = self.model(email=self.normalize_email(email))
		
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, password):
		user = self.create_user(email, password)
		
		user.is_admin = True
		user.save(using=self._db)
		return user


class CustomUser(AbstractBaseUser):
	email = models.EmailField(
		verbose_name = 'email address',
		max_length   = 255,
		unique       = True
	)
	is_active = models.BooleanField(default=True)
	is_admin  = models.BooleanField(default=False)
	
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


simple_audit.register(Foobar)
