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
		fields = ['id','file_url']
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
		myobject['voice_profile_name']=str(instance.voice_profile)
		myobject['title']=instance.title
		#replace all spaces with underscores
		#formatted_file_name=str(instance.title).replace(" ", "_")
		file_name_to_be_saved=instance.title.strip() + "(" + str(instance.voice_profile)+")"
		file_name_to_be_saved=file_name_to_be_saved.replace(" ", "_")
		myobject['track_file_name']=file_name_to_be_saved

		formatted_file_name=str(instance.title).replace(" ", "_")
		
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
		print("**** Request Here *****")
		print(json_data)
		headers = {'Content-type': 'application/json'}
		response=requests.post(base.COMBINER_ENDPOINT,data=json_data, headers=headers)
		#jsonresponse=json.load(io.BytesIO(response.content))
		jsonresponse=json.load(io.BytesIO(response.content))
		print("**** Response Here *****")
		print(jsonresponse)
		instance.duration=jsonresponse.get("duration",2)
		track_file_name=jsonresponse.get("track_file_name")
		instance.audio_file=track_file_name
		track_fileURL=base.GOOGLE_CLOUD_STORAGE_BASE_URL+"/"+base.TTS_BUCKET_NAME+"/"+track_file_name
		instance.file_url=track_fileURL
		instance.processed=True

		processed_tracks=jsonresponse.get("processed_tracks", [])

		for processed_track in processed_tracks:
			# There could be some of the tracks which could be unprocessed
			# The user may have not listened to them. 
			# We can prevent reconverting these to audio again, unless they are updated again.

			#The combine operation gets us all the data for the unprocessed tracks.

			track_text_id=processed_track.get("id")
			unprocessed_track_text=TrackText.objects.get(id=track_text_id)
			unprocessed_track_text.duration=processed_track.get("duration")
			file_name=processed_track.get("file_name")
			unprocessed_track_text.audio_file_name=file_name
			fileURL=base.GOOGLE_CLOUD_STORAGE_BASE_URL+"/"+base.TTS_BUCKET_NAME+"/"+file_name
			unprocessed_track_text.audio_file=fileURL
			unprocessed_track_text.processed=True
			unprocessed_track_text.save()



		instance.save()
		return instance

		
		