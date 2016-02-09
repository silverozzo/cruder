from django                     import forms
from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms  import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group, Permission
from guardian.admin             import GuardedModelAdmin
from guardian.decorators        import permission_required_or_403
from guardian.shortcuts         import get_objects_for_user

from django.db.models.query import QuerySet

from rest_condition             import ConditionalPermission, Or

from .models import CustomUser, Organization, Team, Teammate

from .permissions import (GuardedOrganizationPermission,
	GuardedTeamPermission, LinkedOrganizationPermission, LinkedTeamPermission)


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
		fields = ('email', 'password', 'is_active', 'organization', 'groups', 'user_permissions')
	
	def clean_password(self):
		return self.initial['password']


class UserAdmin(BaseUserAdmin):
	form     = UserChangeForm
	add_form = UserCreationForm
	
	list_display  = ('email', 'is_staff', 'is_superuser', 'organization')
	fieldsets     = (
		(None,           {'fields': ('email', 'password', 'is_staff', 'is_superuser', 'organization', 'groups', 'user_permissions')}),
		('persmissions', {'fields': ('is_staff',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('email', 'password1', 'password2', 'organization'),
		}),
	)
	search_fields = ('email',)
	ordering      = ('email',)


class OrganizationAdmin(GuardedModelAdmin):
	list_display  = ('name',)
	search_fields = ('name',)
	ordering      = ('name',)
	
	def get_queryset(self, request):
		result = super(OrganizationAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return result
		
		allowed     = get_objects_for_user(request.user, 'first.view_organization', accept_global_perms=False)
		allowed_ids = map(lambda x: x.pk, allowed)
		if request.user.organization:
			allowed_ids.append(request.user.organization.pk)
		
		return result.filter(pk__in=allowed_ids)


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

admin.site.register(Permission)
