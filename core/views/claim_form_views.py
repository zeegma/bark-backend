from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import re
import json
from supabase import create_client, Client
from datetime import datetime

from core.models import LostItem, ClaimForm

# Claim Form GET
def get_claim_forms(request):

    items = ClaimForm.objects.all().values()
    return JsonResponse(list(items), status=200, safe=False)

# Claim Form POST
@csrf_exempt
def create_claim_form(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Only POST allowed."}, status=405)

    try:
        # Parse JSON from the request body
        data = json.loads(request.body)

        # Get item instance
        try:
            item = LostItem.objects.get(id=data.get('item_id'))
        except LostItem.DoesNotExist:
            return JsonResponse({"message": "Lost item not found."}, status=404)

        # Create a new ClaimForm
        claim = ClaimForm.objects.create(
            request_date=data.get('request_date'),
            name=data.get('name'),
            ownership_photo=data.get('ownership_photo'),
            detailed_description=data.get('detailed_description'),
            number=data.get('number'),
            media=data.get('media'),
            item_id=item
        )

        return JsonResponse({"message": "Claim form submitted successfully."}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    



# # Create a supabase connection
# def create_supabase_instance():
#     url: str = os.environ.get('SUPABASE_URL')
#     key: str = os.environ.get('SUPABASE_KEY')

#     supabase: Client = create_client(url, key)

#     return supabase

# # Upload photo to Supabase and return URL
# def upload_photo_supabase(image):
#     supabase = create_supabase_instance()
#     image_data = image.read()

#     # Get last uploaded image name
#     response = (
#         supabase.storage
#         .from_("claim-form-photos")
#         .list(
#             "",
#             {
#                 "limit": 1,
#                 "offset": 0,
#                 "sortBy": {"column": "name", "order": "desc"},
#             }
#         )
#     )

#     # Get the name of the last item and find what numbers it has
#     item_count = re.findall(r'\d+', response[0].get('name')) if response else [0]

#     # Convert said count to integer and increment for new file
#     item_count = int(item_count[0])

#     # Create a new image name using item count + 1
#     image_name = "ownership_photo_" + str(item_count + 1) + "." + image.content_type.split('/')[1]

#     # Upload the image to Supabase
#     try:
#         supabase.storage.from_("claim-form-photos").upload(
#                 file=image_data,
#                 path=image_name,
#                 file_options={"content-type": image.content_type}
#             )
#     except:
#         return -1

#     # Get the public URL of the uploaded image
#     url_response = (
#         supabase.storage
#         .from_("claim-form-photos")
#         .get_public_url(image_name)
#     )

#     return url_response