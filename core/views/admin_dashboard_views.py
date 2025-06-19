from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.models import LostItem

# Dashboard Get
@csrf_exempt
@permission_classes([IsAuthenticated])
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
@csrf_exempt
@permission_classes([IsAuthenticated])
def total_items(request):
    """Endpoint for total items count"""
    try:
        count = LostItem.objects.count()
        return JsonResponse({"total": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Unclaimed Total Items
@login_required
@permission_classes([IsAuthenticated])
def lost_items(request):
    """Endpoint for unclaimed/lost items count"""
    try:
        count = LostItem.objects.filter(status=LostItem.Status.UNCLAIMED).count()
        return JsonResponse({"lost": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# Claimed Total Items
@login_required
@permission_classes([IsAuthenticated])
def claimed_items(request):
    """Endpoint for claimed items count"""
    try:
        count = LostItem.objects.filter(status=LostItem.Status.CLAIMED).count()
        return JsonResponse({"claimed": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Expried Total Items
@login_required
@permission_classes([IsAuthenticated])
def expired_items(request):
    """Endpoint for expired items count"""
    try:
        count = LostItem.objects.filter(status=LostItem.Status.EXPIRED).count()
        return JsonResponse({"expired": count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)