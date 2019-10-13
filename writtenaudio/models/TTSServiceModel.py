from django.db import models
import uuid

class TTSService(models.Model):

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
	pass