from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

class CustomUser(AbstractUser):
    pass
    # add additional fields in here
    def __str__(self):
    	if(self.first_name is None or self.first_name==''):
    		return self.username
    	else:
    		return self.first_name + " " +self.last_name
