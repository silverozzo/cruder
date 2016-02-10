from django                     import forms
from django.contrib.auth.forms  import ReadOnlyPasswordHashField

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm',  widget=forms.PasswordInput)
	
	class Meta:
		model  = CustomUser
		fields = ('email', 'organization')
	
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('password not confirmed')
		return password2
	
	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data.get('password1'))
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()
	
	class Meta:
		model  = CustomUser
		fields = ('email', 'password', 'is_active', 'organization', 'groups', 'user_permissions')
	
	def clean_password(self):
		return self.initial['password']
