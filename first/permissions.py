from guardian.core              import ObjectPermissionChecker
from rest_condition             import ConditionalPermission, Or
from rest_framework.permissions import BasePermission

from .models import CustomUser, Organization, Team, Teammate


class OrganizationAccessPermission(BasePermission):
	def has_object_permission(self, request, view, object):
		guard = ObjectPermissionChecker(request.user)
		print('-----')
		print('check organization: ' + str(object))
		perms = guard.get_perms(object)
		print(perms)
		
		if request.user.organization == object:
			return True
		return False
