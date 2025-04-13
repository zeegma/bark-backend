from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import re
import json
from supabase import create_client, Client
from datetime import datetime

from core.models import LostItem, ClaimForm

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
