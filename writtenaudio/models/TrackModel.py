from django.db import models
import uuid
from django.conf import settings
from writtenaudio.models import TTSServiceModel
from writtenaudio.models import LanguageModel
from writtenaudio.models import MusicTrackModel

class Track(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title=models.CharField(max_length=200, default='')
	audio_file=models.CharField(max_length=300,default='', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	processed=models.BooleanField(default=False)
	duration=models.IntegerField(blank=True, null=True)
	voice_profile=models.ForeignKey(TTSServiceModel.TTSService, on_delete=models.CASCADE, blank=True, null=True)
	podcast_mode=models.BooleanField(default=False)
	file_url=models.CharField(max_length=300,default='', blank=True)
	audio_speed=models.FloatField(blank=True, null=True, default=1)
	audio_pitch=models.IntegerField(blank=True, null=True, default=1)
	language=models.ForeignKey(LanguageModel.Language, on_delete=models.CASCADE, blank=True, null=True)
	cloned=models.BooleanField(default=False)
	musictrack=models.ForeignKey(MusicTrackModel.MusicTrack, on_delete=models.CASCADE, blank=True, null=True)
	
	class Meta:
		ordering=['-updated_at']
	def __str__(self):
		return self.title