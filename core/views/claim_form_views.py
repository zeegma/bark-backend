from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .helpers.item_helpers import upload_photo_supabase, delete_photo_supabase

from core.models import LostItem, ClaimForm

# Claim Form GET
def get_claim_forms(request):
    claim_forms = ClaimForm.objects.select_related('item_id').all()

    response_data = []
    for claim in claim_forms:
        response_data.append({
            "id": claim.id,
            "request_date": claim.request_date,
            "name": claim.name,
            "ownership_photo": claim.ownership_photo,
            "detailed_description": claim.detailed_description,
            "number": claim.number,
            "media": claim.media,
            "item_id": claim.item_id.id,
            "item_name": claim.item_id.name,     
            "item_image_url": claim.item_id.photo_url
        })

    return JsonResponse(response_data, status=200, safe=False)

# Claim Form POST
@csrf_exempt
def create_claim_form(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Only POST allowed."}, status=405)

    try:
        # Processes the image, uploads to Supabase
        # Also returns the url of the image from Supabase
        image_url = upload_photo_supabase(request.FILES['image'], bucket="ownership-photo")

        # If same item or same name exists in database
        if image_url == -1:
            return JsonResponse({"message": "Item name already exists in database."}, status=405)

        # Convert JSON string to dictionary
        data = json.loads(request.POST['data'])
        data['ownership_photo'] = image_url
        data['item_id'] = LostItem.objects.get(id=data['item_id'])

        claim = ClaimForm(**data)
        claim.save()

        return JsonResponse({"message": "Claim form submitted successfully."}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
