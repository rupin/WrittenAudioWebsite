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

from django.http import HttpResponseRedirect

def ViewMyTracks(request):
    user=request.user
    template = loader.get_template('mytracks.html')
    mytracks=Track.objects.filter(user=user)
    #print(mytracks.count())
    context = {
       'tracks':mytracks,
       'trackcount':mytracks.count(),
       'user':user,
       'page_title': 'View My Tracks'
    }
    return HttpResponse(template.render(context, request))

def CreateTrack(request):
  template = loader.get_template('createtrackview.html')
  user=request.user
  if request.method == 'GET':
    context = {

    'user':user,
    'page_title': 'Create Track'
    }
    return HttpResponse(template.render(context, request))

  if request.method=='POST':
    tracktitle=request.POST.get("tracktitle", "")
    outputformat=request.POST.get('outputformat', "")
    #print(tracktitle)
    #print(outputformat)
    context={'user':user}
    createdTrack=Track.objects.create(user=user, title=tracktitle, duration=0, output_format=outputformat)
    trackID=str(createdTrack.id)
    return HttpResponseRedirect('/editTrack/'+trackID)
    

	

def EditTrack(request,trackid):
    user=request.user    
    mytrack=Track.objects.get(user=user, id=trackid)
    myTrackText=TrackText.objects.filter(track=trackid).prefetch_related('voice_profile')
    template = loader.get_template('edit_track_view.html')
    #print(mytracks.count())
    context = {
       'track':mytrack,
       'tracktextlist':myTrackText,      
       'user':user,
       'page_title': mytrack.title,
       'track_section_count':myTrackText.count()
       

    }
    return HttpResponse(template.render(context, request))

def ViewTrack(request,trackid):
    user=request.user    
    mytrack=Track.objects.get(user=user, id=trackid)
    myTrackText=TrackText.objects.filter(track=trackid).prefetch_related('voice_profile')
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