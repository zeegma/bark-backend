from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import re
import json
from supabase import create_client, Client
from datetime import datetime

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
    

# Creates a supabase connection
def create_supabase_instance():
    url: str = os.environ.get('SUPABASE_URL')
    key: str = os.environ.get('SUPABASE_KEY')

    supabase: Client = create_client(url, key)

    return supabase


# Uploads image from request to supabase
def upload_photo_supabase(image):
    supabase = create_supabase_instance()
    image_data = image.read()

    # Get last uploaded image name
    response = (
        supabase.storage
        .from_("lost-item-images")
        .list(
            "",
            {
                "limit": 1,
                "offset": 0,
                "sortBy": {"column": "name", "order": "desc"},
            }
        )
    )

    # Get the name of the last item, and find what numbers it has
    item_count = re.findall(r'\d+', response[0].get('name'))

    # Convert said count to integer
    item_count = int(item_count[0])

    # Create string name with prefix, item count + 1, and content_type
    image_name = "image_" + str(item_count + 1) + "." + image.content_type.split('/')[1]

    # Upload image to supabase
    try:
        supabase.storage.from_("lost-item-images").upload(
                file=image_data,
                path=image_name,
                file_options={"content-type": image.content_type}
            )
    except:
        return -1
    
    # Takes the working URL of the recently uploaded image for storing
    url_response = (
        supabase.storage
        .from_("lost-tiem-images")
        .get_public_url(image.name)
    )

    return url_response