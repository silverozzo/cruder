from guardian.core              import ObjectPermissionChecker
from guardian.shortcuts         import get_objects_for_user
from rest_condition             import ConditionalPermission, Or
from rest_framework.permissions import BasePermission

from .models import CustomUser, Organization, Team, Teammate


class OrganizationAccess:
	@staticmethod
	def queryset(user, original_queryset=None):
		if user.is_superuser:
			return original_queryset or Organization.objects.all()
		
		allowed = get_objects_for_user(user, 'first.view_organization', accept_global_perms=False)
		if allowed.exists():
			return allowed
		
		if user.organization:
			return Organization.objects.filter(pk=user.organization.pk)
		
		return allowed.none()
	
	@staticmethod
	def can_change(user, obj=None):
		if user.is_superuser:
			return True
		
		if user.has_perm('first.change_organization') and request.user.has_perm('first.change_organization', obj):
			return True
		
		return user.organization and obj and user.organization.pk == obj.pk
	
	@staticmethod
	def can_delete(user, obj=None):
		if user.is_superuser:
			return True
		
		if user.has_perm('first.delete_organization') and request.user.has_perm('first.delete_organization', obj):
			return True
		
		return user.organization and obj and user.organization.pk == obj.pk


class TeamAccess:
	@staticmethod
	def queryset(user, original_queryset=None):
		if user.is_superuser:
			return original_queryset or Team.objects.all()
		
		return original_queryset or Team.objects.all()
	
	@staticmethod
	def can_change(user, obj=None):
		return True
	
	@staticmethod
	def can_delete(user, obj=None):
		return True


class TeammateAccess:
	@staticmethod
	def queryset(user, original_queryset=None):
		return original_queryset or Teammate.objects.all()
	
	@staticmethod
	def can_change(user, obj=None):
		return True
	
	@staticmethod
	def can_delete(user, obj=None):
		return True


class GuardedOrganizationPermission(BasePermission):
	def has_object_permission(self, request, view, obj):
		guard = ObjectPermissionChecker(request.user)
		if guard.has_perm('view_organization', obj):
			return True
		
		return False


class GuardedTeamPermission(BasePermission):
	def has_object_permission(self, request, view, obj):
		guard = ObjectPermissionChecker(request.user)
		if guard.has_perm('view_team', obj):
			return True
		
		return False


class LinkedOrganizationPermission(BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.user.organization == obj:
			return True
		
		return False


class LinkedTeamPermission(BasePermission):
	def has_object_permission(self, request, view, obj):
		print('linked team permission')
		if request.user.organization == obj.organization:
			return True
		
		return False
