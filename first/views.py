from django.core.urlresolvers         import reverse_lazy
from django.views                     import generic
from rest_framework                   import viewsets
from restfw_composed_permissions.base import BaseComposePermission

from .models      import CustomUser, Foobar, Organization, Team, Teammate
from .serializers import (CustomUserSerializer, FoobarSerializer, 
	OrganizationSerializer, TeamSerializer, TeammateSerializer)


class IndexView(generic.ListView):
	template_name       = 'first/index.html'
	context_object_name = 'foobars'
	
	def get_queryset(self):
		return Foobar.objects.all()


class CreateView(generic.CreateView):
	model       = Foobar
	fields      = ['content_text', 'counter']
	success_url = reverse_lazy('first:index')


class UpdateView(generic.UpdateView):
	model       = Foobar
	fields      = ['content_text', 'counter']
	success_url = reverse_lazy('first:index')


class DeleteView(generic.DeleteView):
	model       = Foobar
	success_url = reverse_lazy('first:index')


class FoobarViewSet(viewsets.ModelViewSet):
	queryset         = Foobar.objects.all()
	serializer_class = FoobarSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
	queryset         = CustomUser.objects.all()
	serializer_class = CustomUserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
	queryset         = Organization.objects.all()
	serializer_class = OrganizationSerializer


class TeamViewSet(viewsets.ModelViewSet):
	queryset         = Team.objects.all()
	serializer_class = TeamSerializer


class TeammateViewSet(viewsets.ModelViewSet):
	queryset         = Teammate.objects.all()
	serializer_class = TeammateSerializer
