from django.core.urlresolvers   import reverse_lazy
from django.views               import generic
from rest_framework             import permissions, viewsets

from .models      import CustomUser, Organization, Team, Teammate
from .permissions import OrganizationAccess, TeamAccess, TeammateAccess
from .serializers import (CustomUserSerializer, 
	OrganizationSerializer, TeamSerializer, TeammateSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
	queryset         = CustomUser.objects.all()
	serializer_class = CustomUserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
	serializer_class = OrganizationSerializer
	
	def get_queryset(self):
		return OrganizationAccess.queryset(self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
	serializer_class = TeamSerializer
	
	def get_queryset(self):
		return TeamAccess.queryset(self.request.user)


class TeammateViewSet(viewsets.ModelViewSet):
	serializer_class = TeammateSerializer
	
	def get_queryset(self):
		return TeammateAccess.queryset(self.request.user)


class OrganizationRestPermission(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		print('object permission called')
		if request.method == 'POST' and obj:
			return OrganizationAccess.can_change(request.user, obj)
		if request.method == 'DELETE':
			return OrganizationAccess.can_delete(request.user, obj)
