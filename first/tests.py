from django.contrib.admin.sites import AdminSite
from django.contrib.auth        import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.http                import HttpRequest
from django.test                import TestCase
from guardian.shortcuts         import assign_perm

from .managers    import CustomUserManager
from .models      import CustomUser, Organization, Team, Teammate
from .admin       import OrganizationAdmin
from .permissions import OrganizationAccess, TeamAccess, TeammateAccess


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


def creating_organization(name='first'):
	company = Organization(name=name)
	company.save()
	
	return company


def creating_team(organization, teamname = 'foobar'):
	team = Team(
		name         = teamname,
		organization = organization
	)
	team.save()
	
	return team


def creating_teammate(team, fullname='foobar'):
	teammate = Teammate(
		fullname = fullname,
		team     = team
	)
	teammate.save()
	
	return teammate


def make_request_with_user(user):
	request = HttpRequest()
	request.user = user
	
	return request


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


class GuardianTests(TestCase):
	def test_assign_object_permission(self):
		company = creating_organization()
		user    = creating_staff_user()
		assign_perm('first.view_organization', user, company)
		self.assertEqual(user.has_perm('first.view_organization', company), True)
	
	def test_assign_global_permission(self):
		company = creating_organization()
		user    = creating_staff_user()
		assign_perm('first.view_organization', user)
		self.assertEqual(user.has_perm('first.view_organization'), True)
		self.assertEqual(user.has_perm('first.view_organization', company), False)


class AdminAccessTests(TestCase):
	def setUp(self):
		self.site = AdminSite()
	
	def test_empty_organization_list_by_staffuser(self):
		user    = creating_staff_user()
		admin   = OrganizationAdmin(Organization, self.site)
		request = make_request_with_user(user)
		self.assertEqual(admin.get_queryset(request).count(), 0)
	
	def test_simple_organization_list_by_staffuser(self):
		fake    = creating_organization()
		user    = creating_staff_user()
		admin   = OrganizationAdmin(Organization, self.site)
		request = make_request_with_user(user)
		self.assertEqual(admin.get_queryset(request).count(), 0)
	
	def test_empty_organization_list_by_superuser(self):
		user      = creating_superuser()
		admin     = OrganizationAdmin(Organization, self.site)
		request   = make_request_with_user(user)
		allowed   = admin.get_queryset(request).count()
		self.assertEqual(allowed, 0)
	
	def test_simple_organization_list_by_superuser(self):
		fake      = creating_organization()
		user      = creating_superuser()
		admin     = OrganizationAdmin(Organization, self.site)
		request   = make_request_with_user(user)
		allowed   = admin.get_queryset(request).count()
		fullcount = Organization.objects.all().count()
		self.assertEqual(allowed, fullcount)
	
	def test_simple_organization_list_by_linked_staffuser(self):
		company = creating_organization()
		user    = creating_staff_user(company)
		admin   = OrganizationAdmin(Organization, self.site)
		request = make_request_with_user(user)
		self.assertEqual(admin.get_queryset(request).count(), 1)
	
	def test_simple_organization_list_by_staffuser_with_view_permission(self):
		company = creating_organization()
		user    = creating_staff_user()
		assign_perm('first.view_organization', user, company)
		
		request = make_request_with_user(user)
		admin   = OrganizationAdmin(Organization, self.site)
		self.assertEqual(admin.get_queryset(request).count(), 1)
	
	def test_simple_organization_list_by_linked_staffuser_with_view_permission(self):
		company = creating_organization()
		second  = creating_organization('second')
		user    = creating_staff_user(company)
		assign_perm('first.view_organization', user, second)
		
		request = make_request_with_user(user)
		admin   = OrganizationAdmin(Organization, self.site)
		self.assertEqual(admin.get_queryset(request).count(), 1)


class OrganizationAccessTests(TestCase):
	def test_get_list_by_staffuser(self):
		user  = creating_staff_user()
		check = OrganizationAccess.queryset(user)
		self.assertEqual(len(check), 0)
	
	def test_get_list_by_linked_staffuser(self):
		company = creating_organization()
		user    = creating_staff_user(company)
		check   = OrganizationAccess.queryset(user)
		self.assertEqual(len(check), 1)
	
	def test_get_list_by_staffuser_with_perm(self):
		first  = creating_organization('first')
		second = creating_organization('second')
		user   = creating_staff_user()
		assign_perm('first.view_organization', user, first)
		assign_perm('first.view_organization', user, second)
		
		check  = OrganizationAccess.queryset(user)
		self.assertEqual(len(check), 2)
	
	def test_get_list_by_linked_staffuser_with_perm(self):
		first  = creating_organization('first')
		second = creating_organization('second')
		third  = creating_organization('third')
		user   = creating_staff_user(third)
		assign_perm('first.view_organization', user, first)
		assign_perm('first.view_organization', user, second)
		
		check  = OrganizationAccess.queryset(user)
		self.assertEqual(len(check), 2)
		self.assertEqual(first in check, True)
		self.assertEqual(second in check, True)
	
	def test_get_empty_list_by_superuser(self):
		user  = creating_superuser()
		check = OrganizationAccess.queryset(user)
		self.assertEqual(len(check), 0)
	
	def test_get_simple_list_by_superuser(self):
		first  = creating_organization('first')
		second = creating_organization('second')
		user   = creating_superuser()
		check  = OrganizationAccess.queryset(user)
		self.assertEqual(len(check), 2)
	
	def test_changing_by_staffuser(self):
		company = creating_organization()
		user    = creating_staff_user()
		check   = OrganizationAccess.can_change(user, company)
		self.assertEqual(check, False)
	
	def test_changing_by_linked_staffuser(self):
		company = creating_organization()
		user    = creating_staff_user(company)
		assign_perm('first.change_organization', user)
		
		self.assertEqual(True, OrganizationAccess.can_change(user, company))
	
	def test_changing_by_linked_staffuser_with_perm(self):
		first  = creating_organization('first')
		second = creating_organization('second')
		user   = creating_staff_user(first)
		assign_perm('first.change_organization', user)
		assign_perm('first.change_organization', user, second)
		
		self.assertEqual(False, OrganizationAccess.can_change(user, first))
		self.assertEqual(True,  OrganizationAccess.can_change(user, second))


class TeamAccessTests(TestCase):
	
	def test_get_empty_list_by_staffuser(self):
		user = creating_staff_user()
		self.assertEqual(0, len(TeamAccess.queryset(user)))
	
	def test_get_simple_list_by_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user()
		self.assertEqual(0, len(TeamAccess.queryset(user)))
	
	def test_get_simple_list_by_linked_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user(company)
		assign_perm('first.view_team', user)
		
		self.assertEqual(1, len(TeamAccess.queryset(user)))
	
	def test_get_simple_list_by_linked_staffuser_with_perm(self):
		first       = creating_organization('first')
		first_team  = creating_team(first, 'first team')
		second      = creating_organization('second')
		second_team = creating_team(second, 'second team')
		user        = creating_staff_user(first)
		assign_perm('first.view_team', user)
		
		check = TeamAccess.queryset(user)
		self.assertEqual(1, len(check))
		self.assertEqual(True, first_team in check)
	
	def test_get_simple_list_by_linked_staffuser_with_perm(self):
		first       = creating_organization('first')
		first_team  = creating_team(first, 'first team')
		second      = creating_organization('second')
		second_team = creating_team(second, 'second team')
		user        = creating_staff_user(first)
		assign_perm('first.view_team', user)
		assign_perm('first.view_organization', user, second)
		
		check = TeamAccess.queryset(user)
		self.assertEqual(1, len(check))
		self.assertEqual(True, second_team in check)
	
	def test_get_empty_list_by_superuser(self):
		user = creating_superuser()
		self.assertEqual(0, len(TeamAccess.queryset(user)))
	
	def test_get_simple_list_by_superuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_superuser()
		self.assertEqual(1, len(TeamAccess.queryset(user)))
	
	def test_changing_by_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user()
		self.assertEqual(False, TeamAccess.can_change(user, team))
	
	def test_changing_by_linked_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user(company)
		self.assertEqual(False, TeamAccess.can_change(user, team))
	
	def test_changing_by_linked_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user(company)
		assign_perm('first.change_team', user)
		self.assertEqual(True, TeamAccess.can_change(user, team))
	
	def test_changing_by_linked_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user()
		assign_perm('first.change_team', user)
		assign_perm('first.view_organization', user, company)
		self.assertEqual(True, TeamAccess.can_change(user, team))
	
	def test_deleting_by_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user()
		self.assertEqual(False, TeamAccess.can_delete(user, team))
	
	def test_deleting_by_linked_staffuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user(company)
		assign_perm('first.delete_team', user)
		self.assertEqual(True, TeamAccess.can_delete(user, team))
	
	def test_deleting_by_staffuser_with_perm(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_staff_user()
		assign_perm('first.delete_team', user)
		assign_perm('first.view_organization', user, company)
		self.assertEqual(True, TeamAccess.can_delete(user, team))
	
	def test_deleting_by_superuser(self):
		company = creating_organization()
		team    = creating_team(company)
		user    = creating_superuser()
		self.assertEqual(True, TeamAccess.can_delete(user, team))


class TeammateAccessTests(TestCase):
	
	def test_get_empty_list_by_staffuser(self):
		user = creating_staff_user()
		self.assertEqual(0, len(TeammateAccess.queryset(user)))
	
	def test_get_simple_list_by_staffuser(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user()
		self.assertEqual(0, len(TeammateAccess.queryset(user)))
	
	def test_simple_list_by_superuser(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_superuser()
		self.assertEqual(1, len(TeammateAccess.queryset(user)))
	
	def test_list_by_linked_staffuser(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user(company)
		self.assertEqual(0, len(TeammateAccess.queryset(user)))
	
	def test_list_by_linked_staffuser_with_global_perm(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user(company)
		assign_perm('first.view_teammate', user)
		self.assertEqual(1, len(TeammateAccess.queryset(user)))
	
	def test_list_by_staffuser_with_perm(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user()
		assign_perm('first.view_teammate', user)
		assign_perm('first.view_organization', user, company)
		self.assertEqual(1, len(TeammateAccess.queryset(user)))
	
	def test_list_by_staffuser_with_perm(self):
		first           = creating_organization('first')
		first_team      = creating_team(first)
		first_teammate  = creating_teammate(first_team)
		second          = creating_organization('second')
		second_team     = creating_team(second)
		second_teammate = creating_teammate(second_team)
		user            = creating_staff_user(first)
		assign_perm('first.view_teammate', user)
		assign_perm('first.view_organization', user, second)
		
		check = TeammateAccess.queryset(user)
		self.assertEqual(1, len(check))
		self.assertEqual(True, second_teammate in check)
	
	def test_changing_by_staffuser(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user()
		self.assertEqual(False, TeammateAccess.can_change(user, teammate))
	
	def test_changing_by_superuser(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_superuser()
		self.assertEqual(True, TeammateAccess.can_change(user, teammate))
	
	def test_changing_by_linked_staffuser(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user(company)
		self.assertEqual(False, TeammateAccess.can_change(user, teammate))
	
	def test_changing_by_linked_staffuser(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user(company)
		assign_perm('first.change_teammate', user)
		self.assertEqual(True, TeammateAccess.can_change(user, teammate))
	
	def test_changing_by_staffuser_with_perm(self):
		company  = creating_organization()
		team     = creating_team(company)
		teammate = creating_teammate(team)
		user     = creating_staff_user()
		assign_perm('first.change_teammate', user)
		assign_perm('first.view_organization', user, company)
		self.assertEqual(True, TeammateAccess.can_change(user, teammate))


class UserCreatingTests(TestCase):
	def test_creating_stuff_user(self):
		manager = CustomUser.objects
		check   = manager.create_user('test@test.com', 'tester')
		user    = authenticate(username='test@test.com', password='tester')
		self.assertEqual(check, user)
	
	def test_login_stuff_user(self):
		manager = CustomUser.objects
		check   = manager.create_user('test@test.com', 'tester')
		user    = authenticate(username='test@test.com', password='tester')
		self.assertEqual(True, user.is_active)
	
	def test_creating_super_user(self):
		manager = CustomUser.objects
		check   = manager.create_superuser('admin@admin.com', 'admin')
		user    = authenticate(username='admin@admin.com', password='admin')
		self.assertEqual(check, user)
		self.assertEqual(True, user.is_superuser)

