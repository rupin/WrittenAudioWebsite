from writtenaudio.models.TrackModel import Track
from rest_framework import generics
from writtenaudio.serializers.TrackSerializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from writtenaudio.permissions.TrackAccessPermission import UserPermittedonTrack

class UpdateTrackAPIView(generics.UpdateAPIView):
	serializer_class = TrackSerializer
	permission_classes = [IsAuthenticated, UserPermittedonTrack]

	def get_queryset(self):        
		return Track.objects.all()
		
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)

class UpdateVoiceProfileAPIView(generics.UpdateAPIView):
	serializer_class = UpdateVoiceProfileSerializer
	permission_classes = [IsAuthenticated,UserPermittedonTrack]

	def get_queryset(self):        
		return Track.objects.all()
		
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)

		

class GenerateCombinedAudio(generics.UpdateAPIView):
	serializer_class=CombineAudioSerializer
	permission_classes = [IsAuthenticated,UserPermittedonTrack]

	def get_queryset(self):        
		return Track.objects.all()
		
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)

		

class TrackResponseTimeoutAPI(generics.UpdateAPIView):

	serializer_class=TrackResponseTimeoutSerializer
	permission_classes = [IsAuthenticated,UserPermittedonTrack]

	def get_queryset(self):        
		return Track.objects.all()
		
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)