from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .helpers.item_helpers import upload_photo_supabase
from core.models import LostItem

# Lost Items GET
def get_lost_items(request):

    items = LostItem.objects.all().values()
    return JsonResponse(list(items), status=200, safe=False)


# Lost Items POST
@csrf_exempt
def create_lost_items(request):

    if request.method != 'POST':
        return JsonResponse({"message": "Only POST allowed."}, status=405)

    # Processes the image, uploads to Supabase
    # Also returns the url of the image from Supabase
    image_url = upload_photo_supabase(request.FILES['image'])

    # If same item or same name exists in database
    if image_url == -1:
        return JsonResponse({"message": "Item name already exists in database."}, status=405)

    # Convert JSON string to dictionary
    data = json.loads(request.POST['data'])

    # Instantiate the item to be saved
    item = LostItem(
        name=data.get('name'),
        description=data.get('description'),
        category=data.get('category'),
        date_found = data.get('date_found'),
        time_found = data.get('time_found'),
        location_found=data.get('location_found'),
        photo_url=image_url,
        status=data.get('status'),
    )
    item.save()
    return JsonResponse({"message": "Item created"}, status=200)


# Lost Items PUT
@csrf_exempt
def edit_lost_items(request, item_id):
    pass

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
    