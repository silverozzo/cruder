from rest_framework import serializers

from .models import CustomUser, Organization, Team, Teammate


class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'organization']


class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Organization
		fields = ['id', 'name']


class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = ['id', 'name', 'organization']


class TeammateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teammate
		fields = ['id', 'fullname', 'team']
