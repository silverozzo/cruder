from guardian.core              import ObjectPermissionChecker
from rest_condition             import ConditionalPermission, Or
from rest_framework.permissions import BasePermission

from .models import CustomUser, Organization, Team, Teammate


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
