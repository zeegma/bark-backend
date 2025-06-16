from django.contrib.auth.hashers import make_password
from core.models import Admin

def run(*args):
    # This script should be run after applying migrations but before using the new auth system
    
    # Get all admins
    admins = Admin.objects.all()
    
    for admin in admins:
        # Hash any plaintext passwords
        if not admin.password.startswith('pbkdf2_sha256$'):  # Check if password is already hashed
            admin.password = make_password(admin.password)
            admin.save()
    
    print(f"Successfully migrated {len(admins)} admin accounts to use hashed passwords")