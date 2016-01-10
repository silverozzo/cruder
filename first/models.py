from django.db import models

# Create your models here.
class Foobar(models.Model):
	content_text = models.CharField(max_length=200)
	counter      = models.IntegerField(default=0)
	extra_file   = models.FileField(upload_to='uploads/')
