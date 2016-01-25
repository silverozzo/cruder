from django.core.urlresolvers import reverse
from django.http              import HttpResponse, HttpResponseRedirect
from django.shortcuts         import get_object_or_404, render
from django.template          import loader, RequestContext
from django.views             import generic

from .models import Foobar


class IndexView(generic.ListView):
	"""
	Page with listing all foobar objects
	"""
	
	template_name       = 'first/index.html'
	context_object_name = 'foobars'
	
	def get_queryset(self):
		return Foobar.objects.all()


def edit(request, pk):
	foobar   = get_object_or_404(Foobar, pk=pk)
	template = loader.get_template('first/edit.html')
	context  = RequestContext(request, {
			'foobar': foobar
		})
	return HttpResponse(template.render(context))


def update(request, pk):
	foobar = get_object_or_404(Foobar, pk=pk)
	print(request.POST['test'])
	return HttpResponseRedirect(reverse('first:edit', args=(foobar.id,)))
