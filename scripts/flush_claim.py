from core.models import ClaimForm

def run(*args):
    # Perform flush
    ClaimForm.objects.all().delete()