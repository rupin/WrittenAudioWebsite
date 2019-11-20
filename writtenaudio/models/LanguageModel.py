
from django.db import models
import uuid
class Language(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	code=models.CharField(max_length=10, blank=False)
	display_name=models.CharField(max_length=40, blank=True, null=True)
	enabled=models.BooleanField(default=False)
	system_default=models.BooleanField(default=False)

	class Meta:
		ordering=['display_name']
	def __str__(self):
		return self.display_name