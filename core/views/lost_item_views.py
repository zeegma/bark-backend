from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.models import LostItem

# Lost Items GET
def get_lost_items(request):
    items = LostItem.objects.all().values()
    return JsonResponse(list(items), status=200, safe=False)

# Lost Items DELETE
@csrf_exempt
def delete_lost_items(request, item_id):
    try:
        item = LostItem.objects.get(id=item_id)
        if item.delete():
            return JsonResponse({"message": "Item deleted."}, status=200)
        else:
            return JsonResponse({"message": "Error deleting item."}, status=405)
    except LostItem.DoesNotExist:
         return JsonResponse({"message": "Item does not exists."}, status=404)