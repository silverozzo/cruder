from django.conf.urls import url

from . import views

urlpatterns = [
#	url(r'^$', views.index, name='index'),
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>[0-9]+)/$',        views.edit,   name='edit'),
	url(r'^update/(?P<pk>[0-9]+)/$', views.update, name='update'),
]
