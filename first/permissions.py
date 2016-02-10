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
		if not user.has_perm('first.change_organization'):
			return False
		if not bool(obj):
			return True
		
		allowed = get_objects_for_user(user, 'first.change_organization', accept_global_perms=False)
		if allowed.exists() and obj in allowed:
			return True
		if allowed.exists() and obj not in allowed:
			return False
		
		return bool(user.organization) and bool(obj) and user.organization.pk == obj.pk
	
	@staticmethod
	def can_delete(user, obj=None):
		if user.is_superuser:
			return True
		
		if user.has_perm('first.delete_organization') and user.has_perm('first.delete_organization', obj):
			return True
		
		return False


class TeamAccess:
	@staticmethod
	def queryset(user, original_queryset=None):
		queryset = original_queryset or Team.objects.all()
		if user.is_superuser:
			return queryset
		
		if not user.has_perm('first.view_team'):
			return queryset.none()
		
		allowed = get_objects_for_user(user, 'first.view_organization', accept_global_perms=False)
		if allowed.exists():
			return queryset.filter(organization__in=allowed.values_list('pk', flat=True))
		
		return queryset.filter(organization=user.organization)
	
	@staticmethod
	def can_change(user, obj=None):
		if user.is_superuser:
			return True
		if not user.has_perm('first.change_team'):
			return False
		if not bool(obj):
			return True
		
		allowed = get_objects_for_user(user, 'first.view_organization', accept_global_perms=False)
		if allowed.exists():
			return obj.organization in allowed
		
		return user.organization and user.organization == obj.organization
	
	@staticmethod
	def can_delete(user, obj=None):
		if user.is_superuser:
			return True
		if not user.has_perm('first.delete_team'):
			return False
		if not bool(obj):
			return True
		
		allowed = get_objects_for_user(user, 'first.view_organization', accept_global_perms=False)
		if allowed.exists():
			return obj.organization in allowed
		
		return user.organization and user.organization == obj.organization


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
