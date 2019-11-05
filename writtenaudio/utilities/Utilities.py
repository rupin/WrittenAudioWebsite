
from writtenaudio.models.TTSServiceModel import TTSService
import json
import requests
from writtenaudio.settings import base
import io
class TrackTextAudioServices():

	def __init__(self, trackTextInstance):
		self.trackTextInstance=trackTextInstance

	def GoogleTTSFunction(self):
		datadict={}
		response=""	
		

		json_data=self.getTrackTextJSON()
		json_data = json.dumps(json_data)

		print(json_data)		
		headers = {'Content-type': 'application/json'}
		
		response=requests.post(base.TTS_END_POINT,data=json_data, headers=headers)
		status_code=response.status_code		

		jsonresponse=json.load(io.BytesIO(response.content))
		
		return jsonresponse, status_code

	def getTrackTextJSON(self):

		TTSServiceObject=self.trackTextInstance.voice_profile
		TrackTTSServiceObject=self.trackTextInstance.track.voice_profile
		default_voice_profile=	TTSService.objects.filter(system_default_profile=True)
		dataDict={}		
		dataDict['filename'] = "track_text_"+str(self.trackTextInstance.id)
		dataDict['sentence'] = self.trackTextInstance.text
		dataDict['object_id'] = str(self.trackTextInstance.id)
		dataDict['bucket_name'] = base.TTS_BUCKET_NAME
		dataDict['audio_speed'] = self.trackTextInstance.track.audio_speed
		dataDict['audio_pitch'] = self.trackTextInstance.track.audio_pitch
		dataDict['is_ssml'] = self.trackTextInstance.is_ssml
		dataDict['file_type'] = 'wav'

		# Check if the Track Text Has a Voice Profile, if yes, grab the 
		# engine name and Language Code. This happens if podcast mode is on
		# for the Track

		# If podcast mode is off, the Track has one common Voice Profile
		# that is associated with the Track Model, and not the Track Text Model

		# It is possible that the Track Also does not have a voice profile
		# so then there will be a default voice profile marked as default in the
		# TTSService Model

		#All you get is three shots!

		if(TTSServiceObject):
			dataDict['engine_name'] = TTSServiceObject.service_voice_model
			dataDict['language_code'] = TTSServiceObject.language_code

		elif (TrackTTSServiceObject):
			dataDict['engine_name'] = TrackTTSServiceObject.service_voice_model
			dataDict['language_code'] = TrackTTSServiceObject.language_code
		else:			
			dataDict['engine_name'] = default_voice_profile[0].service_voice_model
			dataDict['language_code'] = default_voice_profile[0].language_code

		#When converting the complete track, some tracks may be unprocessed.
		# We want to have the raw dictionary when appending to that request

		# But if the Track Text is being processed individually, the JSON is required
		
		return dataDict
		
			


		
		
		
