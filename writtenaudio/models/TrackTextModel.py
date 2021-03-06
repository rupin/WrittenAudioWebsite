from django.db import models
import uuid
from django.conf import settings
from writtenaudio.models import TrackModel

from writtenaudio.models import TTSServiceModel

class TrackText(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	#user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	time_marker=models.IntegerField(default=0, blank=False)
	text=models.CharField(max_length=2000, blank=False)
	audio_file=models.CharField(max_length=300,default='', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	processed=models.BooleanField(default=False)
	duration=models.FloatField(blank=True, null=True, default=0)
	voice_profile=models.ForeignKey(TTSServiceModel.TTSService, on_delete=models.CASCADE, blank=True, null=True)
	track=models.ForeignKey(TrackModel.Track, on_delete=models.CASCADE, blank=True, null=True)
	mark_for_deletion=models.BooleanField(default=False)
	audio_file_name=models.CharField(max_length=100,default='', blank=True)
	is_ssml=models.BooleanField(default=False)
	parent_track_text=models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	editable=models.BooleanField(default=True)
	class Meta:
		ordering=['time_marker', 'track']
		verbose_name = "Track Text"