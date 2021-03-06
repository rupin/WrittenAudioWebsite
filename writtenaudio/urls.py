"""writtenaudio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from writtenaudio.views import TrackView
from writtenaudio.views import TrackTextViews
from writtenaudio.views import HomePageViews
from writtenaudio.views import VoiceProfileViews
from writtenaudio.views import DomainVerification
from writtenaudio.api import TrackTextAPI
from writtenaudio.api import TrackAPI
from django.conf.urls import url

import uuid

from django.conf.urls.static import static

from django.contrib.staticfiles.views import serve

from django.views.decorators.cache import never_cache

from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('mytracks/', TrackView.ViewMyTracks),
    #path('createtrack/', TrackView.CreateTrack),
    path('editTrack/<uuid:trackid>', TrackView.EditTrack),
    path('deleteTrack/<uuid:trackid>', TrackView.DeleteTrack),
    path('', HomePageViews.HomePage),
    path('viewTrack/<uuid:trackid>', TrackView.ViewTrack),
    path('CreateTrackEmptyRow/<uuid:trackid>', TrackTextViews.CreateTrackEmptyRow),
    path('deleteTrackText/<uuid:tracktextid>', TrackTextViews.DeleteTrackText),
    path('createtrack/', TrackView.CreateEmptyTrack),
    path('downloadTrack/<uuid:trackid>/', TrackView.DownloadTrack),
    path('downloadTrackText/<uuid:trackTextid>/', TrackTextViews.DownloadTrackText),
    path('voiceProfiles/', VoiceProfileViews.ViewVoiceProfile),
    path('voiceProfiles/<str:accent>', VoiceProfileViews.ViewVoiceProfile),
    
    # Temporary
    
    #path('.well-known/acme-challenge/<str:param>', DomainVerification.verify),



    

    #APIS
    path('updateTrackText/<uuid:pk>/', TrackTextAPI.UpdateTrackTextAPIView.as_view(),),
    path('updateTrack/<uuid:pk>/', TrackAPI.UpdateTrackAPIView.as_view(),),
    path('generateAudio/<uuid:pk>/', TrackTextAPI.UpdateAudio.as_view(),),
    path('CombinedAudioTrack/<uuid:pk>/', TrackAPI.GenerateCombinedAudio.as_view(),),
    path('updateVoiceProfile/<uuid:pk>/', TrackAPI.UpdateVoiceProfileAPIView.as_view(),),
    path('isTrackResultAvailable/<uuid:pk>/', TrackAPI.TrackResponseTimeoutAPI.as_view(),),
    path('translateTrack/<uuid:pk>/', TrackAPI.TranslateTrack.as_view(),),

    
    
]


urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, view=never_cache(serve))


    