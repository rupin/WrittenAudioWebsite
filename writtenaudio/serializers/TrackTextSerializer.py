from rest_framework import serializers
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TrackModel import Track
from writtenaudio.utilities.Utilities import TrackTextAudioServices


class TrackTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackText
		fields = ['id','time_marker', 'text', 'voice_profile', 'processed', 'mark_for_deletion']

	def update(self, instance, validated_data):

		instance.save()
		TrackUpdateData={}
		TrackUpdateData['processed']=False
		AssociatedTrack=Track.objects.filter(id=instance.track.id).update(**TrackUpdateData)
		instance.__dict__.update(**validated_data)
		instance.save()
		return instance

		
	

class AudioCreationSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackText
		fields = ['id','audio_file', 'duration', 'processed','time_marker']
		read_only=['duration']

	def update(self, instance, validated_data):

		if(not instance.processed):
			TTSOnlineService=TrackTextAudioServices(instance)		
			value, status=TTSOnlineService.GoogleTTSFunction()
			if(status==200):		
				instance.processed=True			
				instance.duration=round(value.get('duration'),3)
				instance.audio_file=value.get('file_url')
				instance.audio_file_name=value.get('file_name')	
			instance.save()
		return instance
		
	

		