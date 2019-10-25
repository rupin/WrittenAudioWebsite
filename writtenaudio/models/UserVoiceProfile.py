from django.db import models
import uuid
from django.conf import settings
from writtenaudio.models import TTSServiceModel

class UserVoiceProfile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	voice_profile=models.ForeignKey(TTSServiceModel.TTSService, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user_default_profile=models.BooleanField(default=False)
	enabled=models.BooleanField(default=False)
	class Meta:
		verbose_name = "User Voice Profile"

	def __str__(self):
		return self.voice_profile