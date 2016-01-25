from django.db import models
import simple_audit


class Foobar(models.Model):
	"""
	Model of foobar entity just for tests and something else.
	"""
	content_text = models.CharField(max_length=200)
	counter      = models.IntegerField(default=0)
	extra_file   = models.FileField(upload_to='uploads/', blank=True)
	
	def __str__(self):
		return self.content_text


simple_audit.register(Foobar)
