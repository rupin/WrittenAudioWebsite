from rest_framework import serializers
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TrackModel import Track
from writtenaudio.utilities.Utilities import TrackTextAudioServices


class TrackTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackText
		fields = ['time_marker', 'text', 'voice_profile', 'processed']
	

class AudioCreationSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackText
		fields = ['audio_file', 'duration', 'processed']

	def update(self, instance, validated_data):
		TTSOnlineService=TrackTextAudioServices(instance)		
		value, status=TTSOnlineService.GoogleTTSFunction()
		if(status==200):		
			instance.processed=True
			
			instance.duration=round(value.get('duration'),3)
			instance.audio_file=value.get('file_url')	
		instance.save()
		return instance
		
	

		