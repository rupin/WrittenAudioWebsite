from django.db import models
import uuid
class MusicTrack(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	genre=models.CharField(max_length=40, blank=True, null=True)
	track_name=models.CharField(max_length=40, blank=True, null=True)
	enabled=models.BooleanField(default=False)
	filename=models.CharField(max_length=300, blank=True, null=True)
	#duration=models.IntegerField(blank=True, null=True)

	class Meta:
		ordering=['track_name']
	def __str__(self):
		return self.track_name