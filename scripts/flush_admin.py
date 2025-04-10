import os
from core.models import Admin

def run(*args):
    # Perform flush
    Admin.objects.all().delete()