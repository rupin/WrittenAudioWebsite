
from writtenaudio.models.TTSServiceModel import TTSService
import json
class TrackTextAudioServices():

	def __init__(self, trackTextInstance):
		self.trackTextInstance=trackTextInstance

	def GoogleTTSFunction(self):
		datadict={}
		datadict['sentence']=self.trackTextInstance.text
		datadict['filename']=str(self.trackTextInstance.id)
		TTSServiceObject=self.trackTextInstance.voice_profile
		datadict['engine_name']=TTSServiceObject.service_voice_model
		datadict['language_code']=TTSServiceObject.language_code
		data=json.dumps(datadict)

		return data, 200
		#print(data)
		
		
