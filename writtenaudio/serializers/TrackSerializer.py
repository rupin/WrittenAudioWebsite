from rest_framework import serializers
from writtenaudio.models.TrackModel import Track
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TTSServiceModel import TTSService
import json
import requests
import io
from writtenaudio.settings import base

from writtenaudio.utilities.Utilities import TrackTextAudioServices
from writtenaudio.utilities.TrackUpdater import TrackUpdater

from google.cloud import storage
from google.oauth2 import service_account

from writtenaudio.settings import base



from .TrackTextSerializer import TrackTextSerializer

from django.db import transaction

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
			raise serializers.ValidationError("Not Allowed")





class UpdateVoiceProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = ['voice_profile', 'audio_speed', 'audio_pitch']
	def validate(self, data):

		trackid=self.instance.id
		user=self.context['request'].user

		TrackCount=Track.objects.filter(user=user, id=trackid).count()
		if(TrackCount==1):
			return data
		else:
			raise serializers.ValidationError("Track Does not Exist")
	def update(self, instance, validated_data):
		new_voice_profile=validated_data["voice_profile"]
		instance.voice_profile=new_voice_profile
		instance.processed=False
		instance.audio_file=""
		instance.file_url=''
		instance.duration=0
		user_audio_speed=validated_data.get("audio_speed",instance.audio_speed)
		user_audio_pitch=validated_data.get("audio_pitch",instance.audio_pitch)
		if not (user_audio_speed==instance.audio_speed):
			instance.audio_speed=user_audio_speed
		if not (user_audio_pitch==instance.audio_pitch):
			instance.audio_pitch=user_audio_pitch
		instance.save()


		# Update All Track Texts
		trackTextDict={}
		trackTextDict['processed']=False
		trackTextDict['duration']=0
		if(not instance.podcast_mode):
			trackTextDict['voice_profile']=new_voice_profile
		trackTextDict['audio_file_name']=''
		trackTextDict['audio_file']=''
		
		TrackTexts=TrackText.objects.filter(track=instance).update(**trackTextDict)
		
		return instance





class CombineAudioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = ['id','file_url','audio_file']
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
		

		if(not instance.processed):			

			myobject['id']=str(instance.id)
			myobject['bucket_name']=base.TTS_BUCKET_NAME
			myobject['voice_profile_name']=str(instance.voice_profile)
			myobject['title']=instance.title
			myobject['audio_speed'] = instance.audio_speed
			myobject['audio_pitch'] = instance.audio_pitch
			music_track=instance.musictrack
			if(music_track):
				myobject['music_file_path'] = music_track.filename
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
			
			# Call the End Point which combines the audio files

			# this usually takes more than 20 seconds. 

			#The endpoint returns back a wellformed JSON.

			headers = {'Content-type': 'application/json'}

			# This request can time out(after 30s), and everything after this does not execute
			# The request returns a 503 timeout

			#The way we handle timeout is as follows

			# 1) The HTTP Post has timed out, but function execution will complete
			# 2) The cloud function will save a JSON file on the same bucket as it normally does
			# 3) The AJAX call will automatically know that the request has timedout
			# 4) In the AJAX call, we must repeatedly check for the presence of the JSON file
			# 5) Once the JSON is available, we can download it and process it. 
			# 6) The processed flag will be set on the track.
			# 6) Once processed, the audio is available, and we can play it.

			response=requests.post(base.COMBINER_ENDPOINT,data=json_data, headers=headers)
			jsonresponse=json.load(io.BytesIO(response.content))			
			track_updater=TrackUpdater(instance, jsonresponse)
			track_updater.updateTrackInstance()
			# Once the instance goes to the TrackUpdater, the object gets copied
			# We query the Track Model again. 
			instance=Track.objects.get(id=instance.id)
			
		return instance

class TrackResponseTimeoutSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = ['id','audio_file', 'processed']
	def validate(self, data):

		trackid=self.instance.id
		user=self.context['request'].user

		TrackCount=Track.objects.filter(user=user, id=trackid).count()
		if(TrackCount==1):
			return data
		else:
			raise serializers.ValidationError("Not Allowed")

	def update(self, instance, validated_data):	

		if(not instance.processed):

			storage_credentials = service_account.Credentials.from_service_account_info(base.GS_CREDENTIALS)

			storage_client = storage.Client(project=base.GS_PROJECT_ID, credentials=storage_credentials)

			json_file_name=str(instance.id) +".json"
			bucket = storage_client.get_bucket(base.TTS_BUCKET_NAME)
			blob = bucket.blob(json_file_name)
			if(blob.exists()): # only if the file exists, do download it.
				f=io.BytesIO()
				blob.download_to_file(f)
				track_json=f.getvalue().decode()
				#print(type(track_json)) 
				jsonresponse=json.loads(track_json)
				track_updater=TrackUpdater(instance, jsonresponse)
				track_updater.updateTrackInstance()
				# Once the instance goes to the TrackUpdater, the object gets copied
				# We query the Track Model again. 
				instance=Track.objects.get(id=instance.id)   
			

		return instance

class TranslateTrackSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Track
		fields = ['id','language']
	def validate(self, data):

		trackid=self.instance.id
		user=self.context['request'].user

		TrackCount=Track.objects.filter(user=user, id=trackid).count()
		if(TrackCount==1):
			return data
		else:
			raise serializers.ValidationError("Not Allowed")

	def update(self, instance, validated_data):
		#print(validated_data)
		request_data={}
		#request_data.target_language=
		target_language=validated_data["language"]
		language_code=target_language.code
		#print(target_language)	
		tracktextslist=[]

		# Lets us make a copy of the track, before translation.
		print(instance.id)
		clone=TrackUpdater(instance)
		newTrack=clone.cloneTrack()

		
		track_texts=TrackText.objects.filter(track=newTrack, mark_for_deletion=False)
		for track_text in track_texts:
			tracktextdict={}
			tracktextdict["sentence"]=track_text.text
			tracktextdict["id"]=str(track_text.id)
			tracktextdict["target_language"]=language_code
			tracktextslist.append(tracktextdict)

		request_data["tracktexts"]=tracktextslist
		json_data = json.dumps(request_data)
		#print(json_data)
		headers = {'Content-type': 'application/json'}

		
		response=requests.post(base.TRANSLATION_ENDPOINT,data=json_data, headers=headers)
		jsonresponse=json.load(io.BytesIO(response.content))
		translations=jsonresponse.get("translations",[])
		for translation in translations:
			track_text_id=translation.get("id")
			track_text=translation.get("sentence")
			track_text_object=TrackText.objects.get(id=track_text_id)
			track_text_object.text=track_text
			track_text_object.processed=False
			track_text_object.duration=0
			track_text_object.save()
		newTrack.language=target_language
		newTrack.title=newTrack.title + "("+target_language.display_name+")"
		newTrack.save()
		return newTrack

		


		
		