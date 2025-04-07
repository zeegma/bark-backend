from django.core.serializers import serialize
from django.http import HttpResponse

from core.models import LostItem

# Lost Items GET
def get_lost_items(request):
    items = LostItem.objects.all()
    data = serialize("json", items)
    return HttpResponse(data, content_type="application/json")