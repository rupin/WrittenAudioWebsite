from writtenaudio.models.TrackTextModel import TrackText
from writtenaudio.models.TrackModel import Track
from rest_framework import permissions

class UserPermittedonTrack(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		
		user=request.user		
		myTrack=Track.objects.filter(id=obj.track.id, user=user)
		if(myTrack.count()==1): #User has access to this track				
			return True
		else:
			return False
		
