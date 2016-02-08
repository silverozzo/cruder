from django.conf.urls import include, url
from rest_framework   import routers

import views

router = routers.DefaultRouter()
router.register(r'customuser',   views.CustomUserViewSet)
router.register(r'organization', views.OrganizationViewSet)
router.register(r'team',         views.TeamViewSet)
router.register(r'teammate',     views.TeammateViewSet)


urlpatterns = [	
	url(r'^api/', include(router.urls)),
]
