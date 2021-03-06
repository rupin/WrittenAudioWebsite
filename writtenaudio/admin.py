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
    list_display = ['time_marker', 'text', 'processed', 'duration', 'voice_profile', 'mark_for_deletion']


class TrackAdmin(ImportExportModelAdmin):   
    
    model = TrackModel.Track
    list_display = ['user','title', 'processed', 'duration', 'language']

class TTSServiceAdmin(ImportExportModelAdmin):   
    
    model = TTSServiceModel.TTSService
    list_display = ['name',
                    'provider',
                    'gender',
                    'accent',
                    'enabled', 
                    'system_default_profile',
                    'cost',
                    'premium_voice',
                    'get_preferred_language']
    def get_preferred_language(self, obj):
        return ",".join([p.display_name for p in obj.preferred_language.all()])

class LanguageModelAdmin(ImportExportModelAdmin):   
    
    model = LanguageModel.Language
    list_display = ['code','display_name']

class MusicTrackModelAdmin(ImportExportModelAdmin):   
    
    model = MusicTrackModel.MusicTrack
    list_display = ['genre','track_name', 'enabled']
	


admin.site.register(CustomUserModel.CustomUser, CustomUserAdmin)
admin.site.register(TrackTextModel.TrackText,TrackTextAdmin)
admin.site.register(TrackModel.Track,TrackAdmin)
admin.site.register(TTSServiceModel.TTSService,TTSServiceAdmin)
admin.site.register(UserVoiceProfileModel.UserVoiceProfile)
admin.site.register(LanguageModel.Language,LanguageModelAdmin)
admin.site.register(MusicTrackModel.MusicTrack,MusicTrackModelAdmin)
