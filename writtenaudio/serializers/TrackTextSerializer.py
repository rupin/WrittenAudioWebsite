from rest_framework import serializers
from writtenaudio.models import TrackTextModel


class TrackTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrackTextModel.TrackText
		fields = ['time_marker', 'text']