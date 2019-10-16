from writtenaudio.models.TrackTextModel import TrackText
from rest_framework import generics
from writtenaudio.serializers.TrackTextSerializer import TrackTextSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UpdateTrackTextAPIView(generics.UpdateAPIView):
	serializer_class = TrackTextSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):        
		return TrackText.objects.all()
		
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)