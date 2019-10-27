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

@login_required
def HomePage(request):
    user=request.user
    template = loader.get_template('home_page_view.html')    
    
    context = {
       
			'user':user,
			'page_title': 'Home',
			'homemenu':'treemenu active',
			'trackmenu':'treemenu',
			'voiceprofilemenu':'treemenu',
			'billingmenu':'treemenu', 
    }
    return HttpResponse(template.render(context, request))