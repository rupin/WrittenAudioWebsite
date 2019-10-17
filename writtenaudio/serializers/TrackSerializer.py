from rest_framework import serializers
from writtenaudio.models.TrackModel import Track

class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = ['title']
	def validate(self, data):

		trackid=self.instance.id
		user=self.context['request'].user

		TrackCount=Track.objects.filter(user=user, id=trackid).count()
		if(TrackCount==1):
			return data
		else:
			raise serializers.ValidationError("finish must occur after start")

		
		