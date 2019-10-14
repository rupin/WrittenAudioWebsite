from django.db import models
import uuid
from django.conf import settings

class Track(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title=models.CharField(max_length=200, default='')
	audio_file=models.FileField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	processed=models.BooleanField(default=False)
	duration=models.IntegerField(blank=True, null=True)
	class Meta:
		ordering=['updated_at']
	def __str__(self):
		return self.title