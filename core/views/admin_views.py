from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Admin

import json

# Admins GET
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admins(request):
    items = Admin.objects.all().values('id', 'name', 'email', 'number', 'last_login')
    return JsonResponse(list(items), status=200, safe=False)

# Admin GET: Retrieve details of specific admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_detail(request, admin_id):
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
@api_view(['POST'])
def register_admin(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Checks if email already exists
        if Admin.objects.filter(email=data.get('email')).exists():
            return JsonResponse({"message": "Account with this email already exists."}, status=400)
        
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
            
            # Generate tokens
            refresh = RefreshToken.for_user(admin)
            
            return JsonResponse({
                "message": "Account successfully created.",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "admin": {
                    "id": admin.id,
                    "name": admin.name,
                    "email": admin.email,
                    "number": admin.number,
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({"message": f"Error creating account: {str(e)}"}, status=400)

    except Exception as e:
        return JsonResponse({"message": f"Error creating admin: {str(e)}"}, status=400)
    
# Admin: Delete admin account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_admin(request, admin_id):
    try:
        admin = Admin.objects.get(id=admin_id)
        
        # Admins only can delete their accounts
        if request.user.id != admin.id and not request.user.is_superuser:
            return JsonResponse({"message": "You do not have permission to delete this account."}, status=403)
            
        if admin.delete():
            return JsonResponse({"message": "Account successfully deleted."}, status=200)
        else:
            return JsonResponse({"message": "Error deleting admin account."}, status=400)
    except Admin.DoesNotExist:
        return JsonResponse({"message": "Account does not exist."}, status=404)
    
# Admin: Login
@api_view(['POST'])
def login_admin(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return JsonResponse({
                "message": "Login successful",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "admin": {
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
    
# Admin: Logout - Blacklist the token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_admin(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return JsonResponse({"message": "Successfully logged out."}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Error during logout: {str(e)}"}, status=400)