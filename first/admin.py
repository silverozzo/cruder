from django                     import forms
from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms  import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from guardian.admin             import GuardedModelAdmin

from .models import CustomUser, Organization, Team, Teammate


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm', widget=forms.PasswordInput)
	
	class Meta:
		model  = CustomUser
		fields = ('email','organization')
	
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
		fields = ('email', 'password', 'is_active', 'is_admin', 'organization', 'groups')
	
	def clean_password(self):
		return self.initial['password']


class UserAdmin(BaseUserAdmin):
	form     = UserChangeForm
	add_form = UserCreationForm
	
	list_display  = ('email', 'is_staff', 'is_admin', 'is_superuser', 'organization')
	list_filter   = ('is_admin',)
	fieldsets     = (
		(None,           {'fields': ('email', 'password', 'is_staff', 'is_admin', 'is_superuser', 'organization', 'groups')}),
		('persmissions', {'fields': ('is_admin',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('email', 'password1', 'password2', 'organization'),
		}),
	)
	search_fields = ('email',)
	ordering      = ('email',)
	filter_horizontal = ()


class OrganizationAdmin(GuardedModelAdmin):
	list_display  = ('name',)
	search_fields = ('name',)
	ordering      = ('name',)


class TeamAdmin(GuardedModelAdmin):
	list_display  = ('name', 'organization')
	search_fields = ('name',)
	ordering      = ('organization',)


class TeammateAdmin(GuardedModelAdmin):
	list_display  = ('fullname', 'team')
	search_fields = ('fullname',)
	ordering      = ('team', 'fullname')


admin.site.register(CustomUser,   UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Team,         TeamAdmin)
admin.site.register(Teammate,     TeammateAdmin)
