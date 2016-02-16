from django.conf.urls import include, url
from rest_framework   import routers

import views

router = routers.DefaultRouter()
router.register(r'customuser',   views.CustomUserViewSet)
router.register(r'organization', views.OrganizationViewSet, base_name='organization')
router.register(r'team',         views.TeamViewSet,         base_name='team')
router.register(r'teammate',     views.TeammateViewSet,     base_name='teammate')


urlpatterns = [	
	url(r'^api/', include(router.urls)),
	
	url(r'^$',        views.index,  name='main_menu'),
	url(r'^login/$',  views.login,  name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	
	url(r'^organization/$',                       views.OrganizationListView.as_view(),   name='organization_list'),
	url(r'^organization/create/$',                views.OrganizationCreateView.as_view(), name='organization_create'),
	url(r'^organization/update/(?P<pk>[0-9]+)/$', views.OrganizationUpdateView.as_view(), name='organization_update'),
	url(r'^organization/delete/(?P<pk>[0-9]+)/$', views.OrganizationDeleteView.as_view(), name='organization_delete'),
	
	url(r'^team/$',                       views.TeamListView.as_view(),   name='team_list'),
	url(r'^team/create/$',                views.TeamCreateView.as_view(), name='team_create'),
	url(r'^team/update/(?P<pk>[0-9]+)/$', views.TeamUpdateView.as_view(), name='team_update'),
	url(r'^team/delete/(?P<pk>[0-9]+)/$', views.TeamDeleteView.as_view(), name='team_delete'),
	
	url(r'^teammate/$',                       views.TeammateListView.as_view(),   name='teammate_list'),
	url(r'^teammate/create/$',                views.TeammateCreateView.as_view(), name='teammate_create'),
	url(r'^teammate/update/(?P<pk>[0-9]+)/$', views.TeammateUpdateView.as_view(), name='teammate_update'),
	url(r'^teammate/delete/(?P<pk>[0-9]+)/$', views.TeammateDeleteView.as_view(), name='teammate_delete'),
]
