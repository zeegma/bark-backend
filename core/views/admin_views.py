from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse

from core.models import Admin

# Admins GET
def get_admins(request):
    items = Admin.objects.all().values()
    return JsonResponse(list(items), status=200, safe=False)