from rest_framework import serializers
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TrackModel import Track


class TrackTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackText
		fields = ['time_marker', 'text', 'voice_profile', 'processed']
	

class AudioCreationSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackText
		fields = ['audio_file', 'duration', 'processed']
		
	

		