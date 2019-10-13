from django.db import models
import uuid
from writtenaudio.models import TTSServiceModel
from django.conf import settings
class VoiceProfile(models.Model):
	profile_name=models.CharField(max_length=20, blank=False, default='')
	TTSService=models.ForeignKey(TTSServiceModel.TTSService, on_delete=models.CASCADE, blank=False, default=0)
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	pass