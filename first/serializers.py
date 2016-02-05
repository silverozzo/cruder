from rest_framework import serializers

from .models import Foobar, Organization, CustomUser, Team, Teammate


class FoobarSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Foobar
		fields = ['id', 'content_text', 'counter']


class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Organization
		fields = ['id', 'name']


class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'email', 'is_active', 'is_admin', 'is_staff', 'organization']


class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = ['id', 'name', 'organization']


class TeammateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teammate
		fields = ['id', 'user', 'team']
