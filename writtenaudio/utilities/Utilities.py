
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
		

		TTSServiceObject=self.trackTextInstance.voice_profile
		TrackTTSServiceObject=self.trackTextInstance.track.voice_profile
		dataDict={}		
		dataDict['filename'] = str(self.trackTextInstance.id)
		dataDict['sentence'] = self.trackTextInstance.text

		
		if(TTSServiceObject):
			dataDict['engine_name'] = TTSServiceObject.service_voice_model
			dataDict['language_code'] = TTSServiceObject.language_code

		elif (TrackTTSServiceObject):
			dataDict['engine_name'] = TrackTTSServiceObject.service_voice_model
			dataDict['language_code'] = TrackTTSServiceObject.language_code
		else:
			default_voice_profile=	TTSService.objects.filter(system_default_profile=True)
			dataDict['engine_name'] = default_voice_profile[0].service_voice_model
			dataDict['language_code'] = default_voice_profile[0].language_code


		json_data = json.dumps(dataDict)
		print(json_data)		
		headers = {'Content-type': 'application/json'}
		
		response=requests.post(base.TTS_END_POINT,data=json_data, headers=headers)
		status_code=response.status_code
		print(response)

		jsonresponse=json.load(io.BytesIO(response.content))
		
		return jsonresponse, status_code
		
		
		
