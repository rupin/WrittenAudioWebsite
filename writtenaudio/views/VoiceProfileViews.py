
from django.template import loader
from django.contrib.auth.decorators import login_required
from writtenaudio.models.TTSServiceModel import TTSService
from writtenaudio.models.UserVoiceProfileModel import UserVoiceProfile
from django.http import HttpResponse

from django.db.models import Count, Min




@login_required
def ViewVoiceProfile(request,accent=None):
    user=request.user
    #print(accent)
    if(accent is None):
      template = loader.get_template('voice_accent_view.html')
    else:
      template = loader.get_template('voice_profile_view.html')
   
    TTSProfiles=[]
    if(accent):
      TTSProfiles=TTSService.objects.filter(enabled=True, accent=accent).values('name','avatar_image_path','voice_profile_description', 'gender', 'accent', 'uservoiceprofile__user_default_profile', 'uservoiceprofile__enabled', 'cost', 'language_code').order_by('cost','name')
      if(TTSProfiles.count()==0):
        return HttpResponse("Not Found", status=404)

       
    accents=TTSService.objects.filter(enabled=True).values('accent').annotate(total=Count('accent'), starts_from=Min('cost')).order_by('accent')
    
    page_title="Voices"
    

    if(accent):
      page_title=accent+ " Voices"
   

    context = {
       'profiles':TTSProfiles,        
       'user':user,
       'accents':accents,
       'page_title': page_title,
       'selected_accent':accent,
       'homemenu':'treemenu',
       'trackmenu':'treemenu',
       'voiceprofilemenu':'treemenu active',
       'billingmenu':'treemenu',
    }
    return HttpResponse(template.render(context, request))