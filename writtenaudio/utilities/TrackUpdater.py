from writtenaudio.models.TrackModel import Track
from writtenaudio.models.TrackTextModel import TrackText
import json
from writtenaudio.settings import base
import io
from django.db import transaction
class TrackUpdater():

	def __init__(self, instance, jsonresponse={}):

		self.trackInstance=instance
		self.jsonresponse=jsonresponse



	def updateTrackInstance(self):
		self.trackInstance.duration=self.jsonresponse.get("duration",2)
		track_file_name=self.jsonresponse.get("track_file_name")
		self.trackInstance.audio_file=track_file_name
		track_fileURL=base.GOOGLE_CLOUD_STORAGE_BASE_URL+"/"+base.TTS_BUCKET_NAME+"/"+track_file_name
		self.trackInstance.file_url=track_fileURL
		self.trackInstance.processed=True
		self.trackInstance.save()	

		processed_tracks=self.jsonresponse.get("processed_tracks", [])

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


	def cloneTrack(self):
		newTrack=self.trackInstance
		originalTrackId=self.trackInstance.id
		
		with transaction.atomic():
			newTrack.duration=0	
			newTrack.processed=False
			newTrack.cloned=True
			newTrack.audio_file=""
			newTrack.file_url=""
			newTrack.pk=None
			newTrack.save()
			newTrackID=newTrack.id
			#print(originalTrackId)
			Track_Texts=TrackText.objects.filter(track=originalTrackId, mark_for_deletion=False)
			#print(Track_Texts.query)
			#print(Track_Texts.count())

			for track_text in Track_Texts:
			    original_track_text=track_text
			    track_text.processed=False
			    track_text.duration=0
			    track_text.editable=False
			    track_text.track=newTrack
			    track_text.audio_file=""
			    track_text.audio_file_name
			    track_text.pk=None
			    
			    track_text.save()
			    #track_text.parent_track_text=original_track_text
			    #track_text.save()
			    #a=1/0 
			return newTrack
