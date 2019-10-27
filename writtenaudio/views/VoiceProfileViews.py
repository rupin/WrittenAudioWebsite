
from django.template import loader
from django.contrib.auth.decorators import login_required
from writtenaudio.models.TTSServiceModel import TTSService
from writtenaudio.models.UserVoiceProfileModel import UserVoiceProfile
from django.http import HttpResponse

from django.db.models import Exists, OuterRef, Count




@login_required
def ViewVoiceProfile(request,accent=None):
    user=request.user
    if(accent):
      template = loader.get_template('voice_profile_view.html')
    else:
      template = loader.get_template('voice_profile_view.html')
    #TTSProfiles=TTSService.objects.filter(uservoiceprofile__user=user).values_list('name', 'provider', 'uservoiceprofile__user_default_profile')
    #TTSProfiles=TTSService.objects.filter(enabled=True)\
     #                           .annotate(is_favorite=Exists(UserVoiceProfile.objects.filter(voice_profile=OuterRef('pk'), user=user)))
    #print(accent)
    TTSProfiles=[]
    if(accent):
      TTSProfiles=TTSService.objects.filter(enabled=True, accent=accent).values('name','avatar_image_path','voice_profile_description', 'gender', 'accent', 'uservoiceprofile__user_default_profile', 'uservoiceprofile__enabled').order_by('name','accent')

    #print(TTSProfiles.query)

    #TTSProfiles=TTSService.objects.filter(enabled=True)
    #UserChosenTTSProfile==UserVoiceProfile.objects.filter(user=user)    
    accents=TTSService.objects.filter(enabled=True).values('accent').annotate(total=Count('accent')).order_by('accent')
    #print(accents.query)
    page_title="Voices"
    if(accent):
      page_title=accent+ " Voices"
   

    context = {
       'profiles':TTSProfiles,        
       'user':user,
       'accents':accents,
       'page_title': page_title,
       'homemenu':'treemenu',
       'trackmenu':'treemenu',
       'voiceprofilemenu':'treemenu active',
       'billingmenu':'treemenu',
    }
    return HttpResponse(template.render(context, request))