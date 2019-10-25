from django.http import HttpResponse
from django.template import loader
from writtenaudio.models import *
from django.conf import settings
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_date 

import datetime
from dateutil.parser import *
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TrackModel import Track

from django.http import HttpResponseRedirect
from writtenaudio.models.TTSServiceModel import TTSService

from google.cloud import storage
from google.oauth2 import service_account

from writtenaudio.settings import base
import tempfile
from django.core.files import File

@login_required
def CreateTrackEmptyRow(request, trackid):
	template = loader.get_template('editable_track_row.html')
	user=request.user
	context={}
	myTrack=Track.objects.filter(user=user,id=trackid)
	if myTrack.count()==1:
		defaultData={'duration':0, 'track':myTrack[0], 'time_marker':0}
		createdTrackText=TrackText(**defaultData)
		createdTrackText.save()
		voiceProfiles=TTSService.objects.all()
		context={
				'tracktextlist':[createdTrackText],
       			'voiceprofiles':voiceProfiles

				} ## UI Expects a List

	return HttpResponse(template.render(context, request))

@login_required
def DeleteTrackText(request, tracktextid):
	user=request.user	
	myTrackText=TrackText.objects.filter(id=tracktextid)
	if(myTrackText.count()==1): #There is a track like this
		myTrack=Track.objects.filter(id=myTrackText[0].track.id, user=user)
		if(myTrack.count()==1): #User has access to this track
			myTrackText[0].mark_for_deletion=True
			return HttpResponse(str(tracktextid), status=200)
		else:
			return HttpResponse('Unauthorized', status=401)
	else:
			
		return HttpResponse('Not Found', status=404)

@login_required
def DownloadTrackText(request,trackTextid):
    user=request.user

    myTrackText=TrackText.objects.get(id=trackTextid)
    storage_credentials = service_account.Credentials.from_service_account_info(base.GS_CREDENTIALS)

    storage_client = storage.Client(project=base.GS_PROJECT_ID, credentials=storage_credentials)

    
    bucket = storage_client.get_bucket(base.TTS_BUCKET_NAME)
    blob = bucket.blob(myTrackText.audio_file_name)
    #f=io.BytesIO()
    tmpdir=tempfile.gettempdir() # prints the current temporary directory
    tempFilePath=tmpdir+"/"+myTrackText.audio_file_name
    blob.download_to_filename(tempFilePath)   
    myFile=open(tempFilePath, 'rb').read()
    response = HttpResponse(myFile)
    response['Content-Type'] = 'audio/mpeg'
    response['Content-Disposition'] = 'attachment; filename='+myTrackText.audio_file_name
    #os.remove(tempFilePath)
    return response