from django.db import models
import uuid
from django.conf import settings
from writtenaudio.models import TrackModel

from writtenaudio.models import VoiceProfileModel

class TrackText(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	#user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	time_marker=models.IntegerField(default=0, blank=False)
	text=models.CharField(max_length=2000, blank=False)
	audio_file=models.FileField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	processed=models.BooleanField(default=False)
	duration=models.IntegerField(blank=True, null=True)
	voice_profile=models.ForeignKey(VoiceProfileModel.VoiceProfile, on_delete=models.CASCADE, blank=True, null=True)
	track=models.ForeignKey(TrackModel.Track, on_delete=models.CASCADE, blank=True, null=True)
	class Meta:
		ordering=['time_marker', 'track']