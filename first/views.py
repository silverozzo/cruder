from django.core.urlresolvers import reverse, reverse_lazy
from django.http              import HttpResponse, HttpResponseRedirect
from django.shortcuts         import get_object_or_404, render
from django.template          import loader, RequestContext
from django.views             import generic

from .models import Foobar


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
