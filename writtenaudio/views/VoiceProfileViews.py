
from django.template import loader
from django.contrib.auth.decorators import login_required
from writtenaudio.models.TTSServiceModel import TTSService
from django.http import HttpResponse






@login_required
def ViewVoiceProfile(request):
    user=request.user
    template = loader.get_template('voice_profile_view.html')
    TTSProfiles=TTSService.objects.filter(enabled=True)    
    accents=TTSService.objects.filter(enabled=True).order_by('accent').values('accent').distinct()
    context = {
       'profiles':TTSProfiles,        
       'user':user,
       'accents':accents,
       'page_title': 'Voices'
    }
    return HttpResponse(template.render(context, request))