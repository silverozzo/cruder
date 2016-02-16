from django.core.urlresolvers import reverse_lazy
from django.shortcuts         import render
from django.views             import generic
from rest_framework           import permissions, viewsets

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


def index(request):
	return render(request, 'first/index.html', {})


class OrganizationListView(generic.ListView):
	template_name       = 'first/organization_list.html'
	context_object_name = 'objects'
	
	def get_queryset(self):
		return OrganizationAccess.queryset(self.request.user)


class OrganizationCreateView(generic.CreateView):
	model       = Organization
	fields      = ['name']
	template_name = 'first/update_form.html'
	success_url = reverse_lazy('first:list')


class OrganizationUpdateView(generic.UpdateView):
	model       = Organization
	fields      = ['name']
	success_url = reverse_lazy('first:organization_list')


class OrganizationDeleteView(generic.DeleteView):
	model       = Organization
	success_url = reverse_lazy('first:organization_list')


class TeamListView(generic.ListView):
	template_name       = 'first/team_list.html'
	context_object_name = 'objects'
	
	def get_queryset(self):
		return TeamAccess.queryset(self.request.user)


class TeamCreateView(generic.CreateView):
	model       = Team
	fields      = ['name']
	template_name = 'first/update_form.html'
	success_url = reverse_lazy('first:team_list')


class TeamUpdateView(generic.UpdateView):
	model       = Team
	fields      = ['name']
	success_url = reverse_lazy('first:team_list')


class TeamDeleteView(generic.DeleteView):
	model       = Team
	success_url = reverse_lazy('first:team_list')


class TeammateListView(generic.ListView):
	template_name       = 'first/teammate_list.html'
	context_object_name = 'objects'
	
	def get_queryset(self):
		return TeammateAccess.queryset(self.request.user)


class TeammateCreateView(generic.CreateView):
	model       = Teammate
	fields      = ['fullname']
	template_name = 'first/update_form.html'
	success_url = reverse_lazy('first:teammate_list')


class TeammateUpdateView(generic.UpdateView):
	model       = Teammate
	fields      = ['fullname']
	success_url = reverse_lazy('first:teammate_list')


class TeammateDeleteView(generic.DeleteView):
	model       = Teammate
	success_url = reverse_lazy('first:teammate_list')
