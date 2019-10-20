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
		# value is a json, status is http status
		#Google TTS Function makes a HTTP Post call to Google Cloud function
		value, status=TTSOnlineService.GoogleTTSFunction()
		if(status==200):		
			instance.processed=True
			#print(value.get('duration'))
			instance.duration=value.get('duration')
			instance.audio_file=value.get('file_url')	
		instance.save()
		return instance
		
	

		