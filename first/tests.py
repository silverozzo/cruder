from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission
from django.http                import HttpRequest
from django.test                import TestCase

from .models import CustomUser, Organization
from .admin  import OrganizationAdmin


def creating_staff_user(organization=None):
	user = CustomUser(
		email        = 'test2example.com',
		is_active    = True,
		is_staff     = True,
		is_superuser = False,
		organization = organization
	)
	user.save()
	
	return user


def creating_superuser(organization=None):
	user = creating_staff_user(organization)
	user.is_superuser = True
	user.save()
	
	return user


def creating_first_organization():
	company = Organization(name='first')
	company.save()
	
	return company


def make_request_with_user(user):
	request = HttpRequest()
	request.user = user
	
	return request


# Create your tests here.
class AuthorizationContribTests(TestCase):
	def test_new_user_creating(self):
		user = creating_staff_user()
		self.assertEqual(user.has_perm('foobar'), False)
	
	def test_new_superuser_creating(self):
		user = creating_superuser()
		self.assertEqual(user.has_perm('foobar'), True)
	
	def test_permission_getting(self):
		perm = Permission.objects.get(codename='add_organization')
		self.assertEqual(perm.codename, 'add_organization')
	
	def test_staffuser_cannot_adding_organization(self):
		user = creating_staff_user()
		self.assertEqual(user.has_perm('add_organization'), False)
	
	def test_staffuser_can_adding_organization(self):
		user = creating_staff_user()
		user.user_permissions.add(Permission.objects.get(codename='add_organization'))
		self.assertEqual(user.has_perm('first.add_organization'), True)


class AdminAccessTests(TestCase):
	def setUp(self):
		self.site = AdminSite()
	
	def test_empty_organization_list_by_staffuser(self):
		user    = creating_staff_user()
		admin   = OrganizationAdmin(Organization, self.site)
		request = make_request_with_user(user)
		self.assertEqual(admin.get_queryset(request).count(), 0)
	
	def test_simple_organization_list_by_staffuser(self):
		fake    = creating_first_organization()
		user    = creating_staff_user()
		admin   = OrganizationAdmin(Organization, self.site)
		request = make_request_with_user(user)
		self.assertEqual(admin.get_queryset(request).count(), 0)
	
	def test_empty_organization_list_by_superuser(self):
		user      = creating_superuser()
		admin     = OrganizationAdmin(Organization, self.site)
		request   = make_request_with_user(user)
		allowed   = admin.get_queryset(request).count()
		fullcount = Organization.objects.all().count()
		
		self.assertEqual(allowed, fullcount)
	
	def test_simple_organization_list_by_superuser(self):
		fake      = creating_first_organization()
		user      = creating_superuser()
		admin     = OrganizationAdmin(Organization, self.site)
		request   = make_request_with_user(user)
		allowed   = admin.get_queryset(request).count()
		fullcount = Organization.objects.all().count()
		
		self.assertEqual(allowed, fullcount)

