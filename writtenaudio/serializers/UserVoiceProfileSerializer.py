from rest_framework import serializers
from writtenaudio.models.UserVoiceProfileModel import UserVoiceProfile
from writtenaudio.models.TTSServiceModel import TTSService
from writtenaudio.utilities.Utilities import TrackTextAudioServices



class UserVoiceProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserVoiceProfile
		fields = ['id', 'enabled', 'voice_profile']

	def update(self, instance, validated_data):
		selectedProfile=validated_data['voice_profile']
		TTSProfile=TTSService.objects.filter(id=selectedProfile)
		if(TTSProfile):
			pass:
		else:
			pass:
		instance.save()		
		return instance