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
from writtenaudio.models.TrackModel import Track
from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TTSServiceModel import TTSService

from django.http import HttpResponseRedirect

import requests
import io
from django.http import FileResponse

import json

from google.cloud import storage
from google.oauth2 import service_account

from writtenaudio.settings import base
import tempfile
from django.core.files import File

@login_required
def ViewMyTracks(request):
    user=request.user
    template = loader.get_template('mytracks.html')
    mytracks=Track.objects.filter(user=user)
    #print(mytracks.count())
    context = {
       'tracks':mytracks,
       'trackcount':mytracks.count(),
       'user':user,
       'page_title': 'My Tracks'
    }
    return HttpResponse(template.render(context, request))

# @login_required
# def CreateTrack(request):
#   template = loader.get_template('createtrackview.html')
#   user=request.user
#   if request.method == 'GET':
#     context = {

#     'user':user,
#     'page_title': 'Create Track'
#     }
#     return HttpResponse(template.render(context, request))

#   if request.method=='POST':
#     tracktitle=request.POST.get("tracktitle", "")
#     outputformat=request.POST.get('outputformat', "")
#     #print(tracktitle)
#     #print(outputformat)
#     context={'user':user}
#     createdTrack=Track.objects.create(user=user, title=tracktitle, duration=0, output_format=outputformat)
#     trackID=str(createdTrack.id)
#     return HttpResponseRedirect('/editTrack/'+trackID)



@login_required
#definitely requires throttling
def CreateEmptyTrack(request):  
  user=request.user
  tracktitle='<Click Here to Edit The Track Title>'
  createdTrack=Track.objects.create(user=user, title=tracktitle, duration=0)
  trackID=createdTrack.id
  defaultTTS=TTSService.objects.filter(system_default_profile=True)
  if(defaultTTS.count()==1):
    createdTrack.voice_profile=defaultTTS[0]
    createdTrack.save()
  createdEmptyTrackText=TrackText.objects.create(track=createdTrack)
  return HttpResponseRedirect('/editTrack/'+str(trackID))
    

	
@login_required
def EditTrack(request,trackid):
    user=request.user    

    mytrack=Track.objects.filter(user=user, id=trackid)

    if(mytrack.count()==1): #There is a track like this   
      print("Authorised to Edit Track")
    else:
      return HttpResponse('Unauthorized', status=401)


    myTrackText=TrackText.objects.filter(track=trackid, mark_for_deletion=False).prefetch_related('voice_profile')
    voiceProfiles=TTSService.objects.filter(enabled=True)
    template = loader.get_template('edit_track_view.html')
    #print(mytracks.count())
    context = {
       'track':mytrack[0],
       'tracktextlist':myTrackText,      
       'user':user,
       'page_title': mytrack[0].title,
       'track_section_count':myTrackText.count(),
       'voiceprofiles':voiceProfiles      

    }
    
    return HttpResponse(template.render(context, request))

@login_required
def ViewTrack(request,trackid):
    user=request.user    
    mytrackObjects=Track.objects.filter(user=user, id=trackid)

    if(mytrackObjects.count()==1): #There is a track like this   
      print("Authorised to Edit Track")
    else:
      return HttpResponse('Unauthorized', status=401)

    mytrack=mytrackObjects[0]
    myTrackText=TrackText.objects.filter(track=trackid,mark_for_deletion=False).prefetch_related('voice_profile')
    template = loader.get_template('view_track_detail_view.html')
    #print(mytracks.count())
    context = {
       'track':mytrack,
       'tracktextlist':myTrackText,      
       'user':user,
       'page_title': mytrack.title,
       'track_section_count':myTrackText.count()
       

    }
    return HttpResponse(template.render(context, request))

@login_required
def DeleteTrack(request,trackid):
    user=request.user

    myTrack=Track.objects.filter(user=user,id=trackid)
    if myTrack.count()==1:
        myTrack.delete()

    return HttpResponseRedirect('/mytracks')

@login_required
def DownloadTrack(request,trackid):
    user=request.user

    mytrackObjects=Track.objects.filter(id=trackid, user=user)

    

    if(mytrackObjects.count()==1): #There is a track like this   
      print("Authorised to Edit Track")
    else:
      return HttpResponse('Unauthorized', status=401)

    myTrack=mytrackObjects[0]

    storage_credentials = service_account.Credentials.from_service_account_info(base.GS_CREDENTIALS)

    storage_client = storage.Client(project=base.GS_PROJECT_ID, credentials=storage_credentials)

    
    bucket = storage_client.get_bucket(base.TTS_BUCKET_NAME)
    blob = bucket.blob(myTrack.audio_file)
    #f=io.BytesIO()
    tmpdir=tempfile.gettempdir() # prints the current temporary directory
    tempFilePath=tmpdir+"/"+myTrack.audio_file
    blob.download_to_filename(tempFilePath)   
    myFile=open(tempFilePath, 'rb').read()
    response = HttpResponse(myFile)
    response['Content-Type'] = 'audio/mpeg'
    response['Content-Disposition'] = 'attachment; filename='+myTrack.audio_file
    #os.remove(tempFilePath)
    return response

    #return HttpResponse("abcd")