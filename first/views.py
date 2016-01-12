from django.http      import HttpResponse
from django.shortcuts import render
from django.template  import RequestContext, loader

from .models import Foobar


def index(request):
	foobars  = Foobar.objects.all()
	template = loader.get_template('first/index.html')
	context  = RequestContext(request, {
		'foobars': foobars
	})
	
	return HttpResponse(template.render(context))
