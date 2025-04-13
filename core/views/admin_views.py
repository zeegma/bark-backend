from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.models import Admin

import json

# Admins GET
def get_admins(request):
    items = Admin.objects.all().values()
    return JsonResponse(list(items), status=200, safe=False)

# Admin POST: Create new admin account
@csrf_exempt
def create_admin(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Only POST allowed."}, status=405)
    
    try:
        data = json.loads(request.body)

        # Checks if email already exists
        if Admin.objects.filter(email = data.get('email')).exists():
            return JsonResponse({"message": "Account with this email already exists."})
        
        # Create new admin
        admin = Admin(
            name = data.get('name'),
            email = data.get('email'),
            number = data.get('number'),
            password = data.get('password')
        )
        admin.save()
        return JsonResponse({"message": "Account successfully created."}, status=201)

    except Exception as e:
        return JsonResponse({"message": f"Error creating admin: {str(e)}"}, status=400)
    
# Admin: Delete admin account
@csrf_exempt
def delete_admin(request, admin_id):
    try:
        admin = Admin.objects.get(id=admin_id)
        if admin.delete():
            return JsonResponse({"message": "Account successfully deleted."}, status=200)
        else:
            return JsonResponse({"message" : "Error deleting admin account."}, status=400)
    except Admin.DoesNotExist:
        return JsonResponse({"message": "Account does not exist."}, status=404)