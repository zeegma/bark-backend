from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import re
import json
from supabase import create_client, Client
from datetime import datetime

from core.models import LostItem, ClaimForm

# Dashboard Get
def dashboard_stats(request):
    """Endpoint for all dashboard statistics"""
    try:
        total_items = LostItem.objects.count()
        lost_items = LostItem.objects.filter(status=LostItem.Status.UNCLAIMED).count()
        claimed_items = LostItem.objects.filter(status=LostItem.Status.CLAIMED).count()
        expired_items = LostItem.objects.filter(status=LostItem.Status.EXPIRED).count()

        data = {
            "total": total_items,
            "lost": lost_items,
            "claimed": claimed_items,
            "expired": expired_items
        }
        
        return JsonResponse(data, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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
    
# Claimed Total Items
def claimed_items(request):
    """Endpoint for claimed items count"""
    try:
        count = LostItem.objects.filter(status=LostItem.Status.CLAIMED).count()
        return JsonResponse({"claimed": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Expried Total Items
def expired_items(request):
    """Endpoint for expired items count"""
    try:
        count = LostItem.objects.filter(status=LostItem.Status.EXPIRED).count()
        return JsonResponse({"expired": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)