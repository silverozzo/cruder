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
]
