from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


from core.models import Admin

import json

# Admins GET
def get_admins(request):
    items = Admin.objects.all().values('id', 'name', 'email', 'number', 'last_login')
    return JsonResponse(list(items), status=200, safe=False)

# Admin GET: Retrive details of specific admin
@csrf_exempt
def admin_detail(request, admin_id):
    if request.method == 'GET':
        try:
            admin = Admin.objects.get(id=admin_id)
            return JsonResponse({
                "id": admin.id,
                "name": admin.name,
                "email": admin.email,
                "number": admin.number,
                "last_login": admin.last_login
            }, status=200)
        except Admin.DoesNotExist:
            return JsonResponse({"message": "Account does not exist."}, status=404)
        
# Admin POST: Create new admin account
@csrf_exempt
def register_admin(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Only POST allowed."}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Checks if email already exists
        if Admin.objects.filter(email = data.get('email')).exists():
            return JsonResponse({"message": "Account with this email already exists."})
        
        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            return JsonResponse({"message": "Password validation failed", "errors": list(e)}, status=400)
        # Create new admin
        try:
            admin = Admin.objects.create_user(
                email=email,
                name=data.get('name'),
                number=data.get('number'),
                password=password
            )
            return JsonResponse({"message": "Account successfully created."}, status=201)
        except Exception as e:
            return JsonResponse({"message": f"Error creating account: {str(e)}"}, status=400)

    except Exception as e:
        return JsonResponse({"message": f"Error creating admin: {str(e)}"}, status=400)
    
# Admin: Delete admin account
@login_required
@csrf_exempt
def delete_admin(request, admin_id):
    if request.method != 'DELETE':
        return JsonResponse({"message": "Only DELETE method allowed."}, status=405)

    try:
        admin = Admin.objects.get(id=admin_id)
        if admin.delete():
            return JsonResponse({"message": "Account successfully deleted."}, status=200)
        else:
            return JsonResponse({"message": "Error deleting admin account."}, status=400)
    except Admin.DoesNotExist:
        return JsonResponse({"message": "Account does not exist."}, status=404)
    
# Admin: Login
@csrf_exempt
def login_admin(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Only POST allowed."}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                "message": "Login successful",
                "admin" : {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "number": user.number,
                }
            }, status=200)
        else:
            return JsonResponse({"message": "Invalid credentials."}, status=401)
            
    except Exception as e:
        return JsonResponse({"message": f"Error during login: {str(e)}"}, status=400)
    
# Admin: Logout
@login_required
def logout_admin(request):
    logout(request)
    return JsonResponse({"message": "Successfully logged out."}, status=200)