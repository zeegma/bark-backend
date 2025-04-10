import os
from core.models import LostItem

def run(*args):
    # Perform flush
    LostItem.objects.all().delete()