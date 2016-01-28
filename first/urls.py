from django.conf.urls import include, url
from rest_framework   import routers

from . import views

router = routers.DefaultRouter()
router.register(r'foobar', views.FoobarViewSet)


urlpatterns = [
	url(r'^$',                       views.IndexView.as_view(),  name='index'),
	url(r'^create/$',                views.CreateView.as_view(), name='create'),
	url(r'^update/(?P<pk>[0-9]+)/$', views.UpdateView.as_view(), name='update'),
	url(r'^delete/(?P<pk>[0-9]+)/$', views.DeleteView.as_view(), name='delete'),
	
	url(r'^api/', include(router.urls)),
]
