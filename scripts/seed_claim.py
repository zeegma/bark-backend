import os

def run(*args):
    # Perform migrations
    os.system("python manage.py migrate")
    
    # Perform data seeding
    os.system("python manage.py loaddata fixtures/claim_data.json")