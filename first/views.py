from django.core.urlresolvers   import reverse_lazy
from django.views               import generic
from rest_framework             import permissions, viewsets

from .models      import CustomUser, Organization, Team, Teammate
from .permissions import OrganizationAccess, TeamAccess, TeammateAccess
from .serializers import (CustomUserSerializer, 
	OrganizationSerializer, TeamSerializer, TeammateSerializer)


class OrganizationRestPermission(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method == 'GET' and obj:
			return OrganizationAccess.can_change(request.user, obj)
		if request.method == 'POST' and obj:
			return OrganizationAccess.can_change(request.user, obj)
		if request.method == 'DELETE' and obj:
			return OrganizationAccess.can_delete(request.user, obj)
		return False


class TeamRestPermission(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method == 'GET' and obj:
			return TeamAccess.can_change(request.user, obj)
		if request.method == 'POST' and obj:
			return TeamAccess.can_change(request.user, obj)
		if request.method == 'DELETE' and obj:
			return TeamAccess.can_delete(request.user, obj)
		return False


class TeammateRestPermission(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method == 'GET' and obj:
			return TeammateAccess.can_change(request.user, obj)
		if request.method == 'POST' and obj:
			return TeammateAccess.can_change(request.user, obj)
		if request.method == 'DELETE' and obj:
			return TeammateAccess.can_delete(request.user, obj)
		return False


class CustomUserViewSet(viewsets.ModelViewSet):
	queryset         = CustomUser.objects.all()
	serializer_class = CustomUserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
	serializer_class   = OrganizationSerializer
	permission_classes = (OrganizationRestPermission,)
	
	def get_queryset(self):
		return OrganizationAccess.queryset(self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
	serializer_class   = TeamSerializer
	permission_classes = (TeamRestPermission,)
	
	def get_queryset(self):
		return TeamAccess.queryset(self.request.user)


class TeammateViewSet(viewsets.ModelViewSet):
	serializer_class   = TeammateSerializer
	permission_classes = (TeammateRestPermission,)
	
	def get_queryset(self):
		return TeammateAccess.queryset(self.request.user)
