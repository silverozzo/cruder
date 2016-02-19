from django.contrib.auth.models import BaseUserManager 


class CustomUserManager(BaseUserManager):
	"""
	Manger for creating users and superusers in auth system
	"""
	def create_user(self, email, password=None):
		"""
		Creating simple user record
		"""
		if not email:
			raise ValueError('email for users is required')
		
		user = self.model(email=self.normalize_email(email))
		
		user.set_password(password)
		user.is_active = True
		user.save(using=self._db)
		
		return user
	
	def create_superuser(self, email, password):
		"""
		Creating user record with admin permissions
		"""
		user = self.create_user(email, password)
		user.is_superuser = True
		user.save(using=self._db)
		
		return user
