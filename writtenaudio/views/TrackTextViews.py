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

def CreateTrackEmptyRow(request, trackid):
	template = loader.get_template('editable_track_row.html')
	user=request.user
	context={}
	myTrack=Track.objects.filter(user=user,id=trackid)
	if myTrack.count()==1:
		defaultData={'duration':0, 'track':myTrack[0], 'time_marker':0}
		createdTrackText=TrackText(**defaultData)
		createdTrackText.save()
		context={'tracktextlist':[createdTrackText]} ## UI Expects a List

	return HttpResponse(template.render(context, request))