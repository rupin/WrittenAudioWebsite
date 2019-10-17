from rest_framework import serializers
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TrackModel import Track


class TrackTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackText
		fields = ['time_marker', 'text', 'voice_profile', 'processed']
	def validate(self, data):

		tracktextid=self.instance.id
		user=self.context['request'].user

		myTrackText=TrackText.objects.filter(id=tracktextid)
		if(myTrackText.count()==1): #There is a track like this
			myTrack=Track.objects.filter(id=myTrackText[0].track.id, user=user)
			if(myTrack.count()==1): #User has access to this track				
				return data
			else:
				raise serializers.ValidationError("finish must occur after start")
		else:
			
			raise serializers.ValidationError("finish must occur after start")