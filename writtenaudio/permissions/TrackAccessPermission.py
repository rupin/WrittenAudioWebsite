from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TrackModel import Track
from rest_framework import permissions
from django.db.models import Q

class UserPermittedonTrack(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		
		user=request.user
		if(type(obj)==TrackText):		
			myTrack=Track.objects.filter(id=obj.track.id, user=user)
			
		elif (type(obj)==Track):
			myTrack=Track.objects.filter(id=obj.id, user=user)
		
		if(myTrack.count()==1): #User has access to this track				
			return True
		else:
			return False