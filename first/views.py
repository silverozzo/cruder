from django.core.urlresolvers   import reverse_lazy
from django.views               import generic
from rest_condition             import ConditionalPermission, Or
from rest_framework             import viewsets

from .models      import CustomUser, Organization, Team, Teammate
from .permissions import OrganizationAccessPermission
from .serializers import (CustomUserSerializer, 
	OrganizationSerializer, TeamSerializer, TeammateSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
	queryset         = CustomUser.objects.all()
	serializer_class = CustomUserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
	queryset           = Organization.objects.all()
	serializer_class   = OrganizationSerializer
	permission_classes = [OrganizationAccessPermission,]


class TeamViewSet(viewsets.ModelViewSet):
	queryset         = Team.objects.all()
	serializer_class = TeamSerializer


class TeammateViewSet(viewsets.ModelViewSet):
	queryset         = Teammate.objects.all()
	serializer_class = TeammateSerializer
