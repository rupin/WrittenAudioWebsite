from writtenaudio.models.UserVoiceProfileModel import UserVoiceProfile
from rest_framework import generics
from writtenaudio.serializers.UserVoiceProfileSerializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class AddRemoveUserVoiceProfile(generics.UpdateAPIView):
	serializer_class = UserVoiceProfileSerializer
	permission_classes = [IsAuthenticated, UserPermittedonTrack]

	def get_queryset(self):        
		return UserVoiceProfile.objects.all()
		
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)		
		return Response(serializer.data)

