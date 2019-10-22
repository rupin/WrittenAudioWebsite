from rest_framework import serializers
from writtenaudio.models.TrackModel import Track
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TTSServiceModel import TTSService
import json
import requests
import io
from writtenaudio.settings import base

from writtenaudio.utilities.Utilities import TrackTextAudioServices

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

class CombineAudioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = ['id','audio_file']
	def validate(self, data):

		trackid=self.instance.id
		user=self.context['request'].user

		TrackCount=Track.objects.filter(user=user, id=trackid).count()
		if(TrackCount==1):
			return data
		else:
			raise serializers.ValidationError("finish must occur after start")

	def update(self, instance, validated_data):

		myobject={}
		tracktexts=[]
		myobject['id']=str(instance.id)
		myobject['bucket_name']=base.TTS_BUCKET_NAME
		
		TrackTexts=TrackText.objects.filter(track=instance, mark_for_deletion=False).prefetch_related('voice_profile')
		
		for trackText in TrackTexts:
			newTrackText={}
			newTrackText["processed"]=trackText.processed
			newTrackText["time_marker"]=trackText.time_marker

			
			if(trackText.processed):
				#If the Track Text is processed, we only send the Audio file and duration
				newTrackText["audio_file"]=trackText.audio_file
				newTrackText["file_name"]=trackText.audio_file_name
				newTrackText["duration"]=trackText.duration
			else:
				TTSOnlineService=TrackTextAudioServices(trackText)
				newTrackText['convertObject']=TTSOnlineService.getTrackTextJSON()		
				
			
						
			
			#print(track)
			tracktexts.append(newTrackText)

		myobject['tracktexts']=tracktexts
		json_data = json.dumps(myobject)
		print(json_data)
		headers = {'Content-type': 'application/json'}
		response=requests.post(base.COMBINER_ENDPOINT,data=json_data, headers=headers)
		#jsonresponse=json.load(io.BytesIO(response.content))
		#print(response.__dict__)
		return instance

		
		