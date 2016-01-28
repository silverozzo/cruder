from rest_framework import serializers

from .models import Foobar


class FoobarSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = Foobar
		fields = ['content_text', 'counter']
