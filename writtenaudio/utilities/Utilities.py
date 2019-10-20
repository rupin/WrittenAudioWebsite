
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
		#dataString=""

		TTSServiceObject=self.trackTextInstance.voice_profile

		dataDict={}



		
		dataDict['filename'] = str(self.trackTextInstance.id)
		dataDict['sentence'] = self.trackTextInstance.text
		dataDict['engine_name'] = TTSServiceObject.service_voice_model
		dataDict['language_code'] = TTSServiceObject.language_code
		json_data = json.dumps(dataDict)
		print(json_data)
		#return "", 400


		
		
		headers = {'Content-type': 'application/json'}
		#print(type(headers))

		#data=json.dumps(datadict)
		#print(base.__dict__)
		response=requests.post(base.TTS_END_POINT,data=json_data, headers=headers)
		status_code=response.status_code
		#print(status_code)
		jsonresponse=json.load(io.BytesIO(response.content))
		#print(jsonresponse.get('duration'))
		#print(type(json.load(jsonresponse)))
		return jsonresponse, status_code
		#print(data)
		
		
