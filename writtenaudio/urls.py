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
from writtenaudio.api import TrackTextAPI
import uuid



urlpatterns = [
    path('admin/', admin.site.urls),
    path('mytracks/', TrackView.ViewMyTracks),
    path('createtrack/', TrackView.CreateTrack),
    path('editTrack/<uuid:trackid>', TrackView.EditTrack),
    path('deleteTrack/<uuid:trackid>', TrackView.DeleteTrack),
    path('', HomePageViews.HomePage),
    path('viewTrack/<uuid:trackid>', TrackView.ViewTrack),
    path('CreateTrackEmptyRow/<uuid:trackid>', TrackTextViews.CreateTrackEmptyRow),
    path('deleteTrackText/<uuid:tracktextid>', TrackTextViews.DeleteTrackText),

    #APIS
    path('updateTrackText/<uuid:pk>/', TrackTextAPI.UpdateTrackTextAPIView.as_view(),),
    
]


urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]


    