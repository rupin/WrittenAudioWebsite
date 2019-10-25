from django.db import models
import uuid

class TTSService(models.Model):
	name=models.CharField(max_length=20, blank=False, default='')
	PROVIDERS = (
						('AMAZON POLLY', 'AMAZON POLLY'),
						("GOOGLE_TTS", "GOOGLE_TTS"),				

				)
	
	provider=models.CharField(max_length=50, choices=PROVIDERS,default="GOOGLE_TTS")


	GENDER = 	(
						('MALE', 'MALE'),
						("FEMALE", "FEMALE"),				

				)
	gender=models.CharField(max_length=20, choices=GENDER, default='MALE')
	service_voice_model=models.CharField(max_length=200, default='')
	accent=models.CharField(max_length=20, default='')
	language_code=models.CharField(max_length=20, default='', blank=True)
	premium_voice=models.BooleanField(default=True)
	cost=models.FloatField(blank=True, null=True, default=0)
	enabled=models.BooleanField(default=False)
	system_default_profile=models.BooleanField(default=False)
	class Meta:
		ordering=['name', 'accent']
		verbose_name = "TTS Service"

	def __str__(self):
		return self.name