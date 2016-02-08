from django.core.urlresolvers   import reverse_lazy
from django.views               import generic
from rest_condition             import ConditionalPermission, Or
from rest_framework             import viewsets

from .models      import CustomUser, Organization, Team, Teammate
from .permissions import (GuardedOrganizationPermission,
	GuardedTeamPermission, LinkedOrganizationPermission, LinkedTeamPermission)
from .serializers import (CustomUserSerializer, 
	OrganizationSerializer, TeamSerializer, TeammateSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
	queryset         = CustomUser.objects.all()
	serializer_class = CustomUserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
	queryset           = Organization.objects.all()
	serializer_class   = OrganizationSerializer
	permission_classes = [
		Or(GuardedOrganizationPermission, LinkedOrganizationPermission),
	]


class TeamViewSet(viewsets.ModelViewSet):
	queryset         = Team.objects.all()
	serializer_class = TeamSerializer
	permission_classes = [
		Or(GuardedTeamPermission, LinkedTeamPermission),
	]


class TeammateViewSet(viewsets.ModelViewSet):
	queryset         = Teammate.objects.all()
	serializer_class = TeammateSerializer
