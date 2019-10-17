from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from writtenaudio.models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

class TrackTextAdmin(ImportExportModelAdmin):   
    
    model = TrackTextModel.TrackText
    list_display = ['time_marker', 'text', 'processed', 'duration', 'voice_profile']


class TrackAdmin(ImportExportModelAdmin):   
    
    model = TrackModel.Track
    list_display = ['user','title', 'processed', 'duration']

class TTSServiceAdmin(ImportExportModelAdmin):   
    
    model = TTSServiceModel.TTSService
    list_display = ['name','provider', 'gender', 'accent']
	


admin.site.register(CustomUserModel.CustomUser, CustomUserAdmin)
admin.site.register(TrackTextModel.TrackText,TrackTextAdmin)
admin.site.register(TrackModel.Track,TrackAdmin)
admin.site.register(TTSServiceModel.TTSService,TTSServiceAdmin)
