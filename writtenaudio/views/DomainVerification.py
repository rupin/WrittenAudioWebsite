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
from writtenaudio.models.LanguageModel import Language

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


def a(request):
    return HttpResponse("cuvlguslwBzUyaIinsA9mqhzJS4OOWcuQusL3W9Q72E.myDJpYgTrvLKjt6SbrmeGN6BxogAuJ12QPUVzGalfvA")
def b(request):
    return HttpResponse("0Y7xhX1JMo-IOI03pceAPYEduVPrCYLz_BqAOwX3pLg.myDJpYgTrvLKjt6SbrmeGN6BxogAuJ12QPUVzGalfvA")