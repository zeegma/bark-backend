from django.core.serializers import serialize
from django.http import HttpResponse

from core.models import ClaimForm

# Sample Function
def controller(request):
    
    return HttpResponse("hello, world")