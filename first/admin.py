from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from guardian.admin             import GuardedModelAdmin
from guardian.decorators        import permission_required_or_403
from rest_condition             import ConditionalPermission, Or

from .forms       import UserChangeForm, UserCreationForm
from .models      import CustomUser, Organization, Team, Teammate
from .permissions import OrganizationAccess, TeamAccess, TeammateAccess


class OrganizationAdmin(GuardedModelAdmin):
	list_display  = ('name',)
	search_fields = ('name',)
	ordering      = ('name',)
	
	def get_queryset(self, request):
		return OrganizationAccess.queryset(request.user, super(OrganizationAdmin, self).get_queryset(request))
	
	def has_change_permission(self, request, obj=None):
		return OrganizationAccess.can_change(request.user, obj)
	
	def has_delete_permission(self, request, obj=None):
		return OrganizationAccess.can_delete(request.user, obj)


class TeamAdmin(GuardedModelAdmin):
	list_display  = ('name', 'organization')
	search_fields = ('name',)
	ordering      = ('organization',)
	
	def get_queryset(self, request):
		return TeamAccess.queryset(request.user, super(TeamAdmin, self).get_queryset(request))
	
	def has_change_permission(self, request, obj=None):
		return TeamAccess.can_change(request.user, obj)
	
	def has_delete_permission(self, request, obj=None):
		return TeamAccess.can_delete(request.user, obj)


class TeammateAdmin(GuardedModelAdmin):
	list_display  = ('fullname', 'team')
	search_fields = ('fullname',)
	ordering      = ('team', 'fullname')
	
	def get_queryset(self, request):
		return TeammateAccess.queryset(request.user, super(TeammateAdmin, self).get_queryset(request))
	
	def has_change_permission(self, request, obj=None):
		return TeammateAccess.can_change(request.user, obj)
	
	def has_delete_permission(self, request, obj=None):
		return TeammateAccess.can_delete(request.user, obj)


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


admin.site.register(CustomUser,   UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Team,         TeamAdmin)
admin.site.register(Teammate,     TeammateAdmin)
admin.site.register(Permission)
