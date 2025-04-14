from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import re
import json
from supabase import create_client, Client
from datetime import datetime

from core.models import LostItem, ClaimForm

# Total Items GET
def total_items(request):
    """Endpoint for total items count"""
    try:
        count = LostItem.objects.count()
        return JsonResponse({"total": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Unclaimed Total Items
def lost_items(request):
    """Endpoint for unclaimed/lost items count"""
    try:
        count = LostItem.objects.filter(status=LostItem.Status.UNCLAIMED).count()
        return JsonResponse({"lost": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)