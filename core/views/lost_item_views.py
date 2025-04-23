from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.multipartparser import MultiPartParser
from django.core.files.uploadhandler import TemporaryFileUploadHandler

import json

from .helpers.item_helpers import upload_photo_supabase, delete_photo_supabase
from core.models import LostItem, ClaimForm

# Lost Items GET
def get_lost_items(request):

    items = LostItem.objects.all().values()
    return JsonResponse(list(items), status=200, safe=False)


# Lost Item Single Item GET
def get_lost_item(request, item_id):

    try:
        item = LostItem.objects.get(id=item_id)

        # Check if there's an accepted claim
        if item.accepted_claim:
            claim_info = item.accepted_claim.id  # Return just the ID if accepted
        else:
            # Return list of all potential claims (not yet accepted)
            claim_info = [
                {
                    "id": claim.id,
                    "name": claim.name,
                    "request_date": claim.request_date.isoformat(),
                    "description": claim.detailed_description,
                }
                for claim in item.claims.all()
            ]

        return JsonResponse({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "category": item.category,
            "date_found": item.date_found,
            "time_found": item.time_found,
            "location_found": item.location_found,
            "photo_url": item.photo_url,
            "status": item.status,
            "claim": claim_info
        }, status=200, safe=False)
    except LostItem.DoesNotExist:
        return JsonResponse({"message": "Item does not exist."}, status=404)


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
    data['photo_url'] = image_url

    # Instantiate the item to be saved
    item = LostItem(**data)
    item.save()
    return JsonResponse({"message": "Item created"}, status=200)


# Lost Items PUT
@csrf_exempt
def edit_lost_items(request, item_id):

    try:
        item_to_edit = LostItem.objects.get(id=item_id)
        old_photo_url = item_to_edit.photo_url
        new_photo_url = None
    except LostItem.DoesNotExist:
        return JsonResponse({"message": "Item not found."}, status=404)

    # If the response has both json data and an image
    if  not request.content_type.startswith('multipart/form-data'):
        return JsonResponse({"message": "Request must be multipart/form-data."}, status=400)

    # Required to handle file uploads
    request.upload_handlers = [TemporaryFileUploadHandler(request)]

    # Initialize parser to get the data and files value
    parser = MultiPartParser(
        request.META,
        request,
        request.upload_handlers,
    )

    # Get the parsed data and files querydict and value
    data, files = parser.parse()

    # Access JSON string
    json_data = json.loads(data['data'])

    # Access image file
    image_file = files.get('image')
    
    # If the image file exists, we try to upload it to Supabase
    if image_file:
        # Upload phase
        uploaded_image_url = upload_photo_supabase(image_file)
        if not uploaded_image_url:
            return JsonResponse({"message": "Error uploading new photo to Supabase."}, status=500)

        # Delete old photo
        if old_photo_url:
            if not delete_photo_supabase(old_photo_url):
                return JsonResponse({"message": "Error deleting old photo from Supabase."}, status=500)
            else:
                print("Photo successfuly deleted.")

        new_photo_url = uploaded_image_url
    else:
        if 'photo_url' in json_data:
            new_photo_url = json_data['photo_url']
        else:
            new_photo_url = old_photo_url
        print("No photo to delete.")

    # Update the photo_url field with the new one
    json_data['photo_url'] = new_photo_url
    
    try:
        # Update items based on the item in the url
        if LostItem.objects.filter(id=item_id).update(**json_data):
            return JsonResponse({"message": "Item updated successfully."}, status=200)
        else:
            return JsonResponse({"message": "Item not found or update failed."}, status=404)
    except Exception as e:
            # Handle any other exceptions that might occur during the update process
        return JsonResponse({"message": f"Database error: {str(e)}"}, status=500)

# Lost Items DELETE
@csrf_exempt
def delete_lost_items(request, item_id):

    try:
        item = LostItem.objects.get(id=item_id)
        claim_form = ClaimForm.objects.filter(item_id=item_id).first()
        item_url = item.photo_url

        # If item has a claim, delete the claim photo as well
        if claim_form and claim_form.ownership_photo:
            claim_photo_url = claim_form.ownership_photo
            print(claim_photo_url)
        
            if item.delete() and delete_photo_supabase(item_url) and delete_photo_supabase(claim_photo_url, "ownership-photo"):
                return JsonResponse({"message": "Item deleted."}, status=200)
            else:
                return JsonResponse({"message": "Error deleting item with claim."}, status=405)
            
        if item.delete() and delete_photo_supabase(item_url):
            return JsonResponse({"message": "Item deleted."}, status=200)
        else:
            return JsonResponse({"message": "Error deleting item."}, status=405)
    except Exception as e:
             # Handle any other exceptions that might occur during the update process
            return JsonResponse({"message": f"Database error: {str(e)}"}, status=500)
    