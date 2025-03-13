from users.models import CustomUser
from django.http import request, HttpResponse

def sample_view(request):
  return HttpResponse("Hello World APII World")