from django.db import models

# Admin Model
class Admin(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField()
    email = models.CharField(unique=True)
    number = models.CharField()
    password = models.CharField()

    class Meta:
        db_table = 'Admin'
        db_table_comment = 'Admin credentials for secure access.'

# Lost Item Model
class LostItem(models.Model):
    
    # Categories for user to select
    class Categories(models.TextChoices):
        # Used to organize choices for category attribute
        ELECTRONICS = 'EL', 'Electronics'
        PERSONAL = 'PB', 'Personal Belongings'
        CLOTHING = 'CL', 'Clothing & Accessories'
        JEWELRY = 'JW', 'Jewelry'
        MISC = 'MS', 'Miscellaneous'

    # Status for user to select
    class Status(models.TextChoices):
        UNCLAIMED = 'UC', 'Unclaimed'
        CLAIMED = 'CL', 'Claimed'
        EXPIRED = 'EX', 'Expired'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField()
    description = models.TextField()
    category = models.CharField(max_length=2, choices=Categories.choices, default=Categories.MISC)
    date_found = models.DateField()
    time_found = models.TimeField()
    location_found = models.TextField()
    photo_url = models.CharField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.UNCLAIMED)

    class Meta:
        db_table = 'LostItem'
        db_table_comment = 'Lost Item Attributes'

# Claim Form Model
class ClaimForm(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_date = models.DateField()
    name = models.CharField()
    ownership_photo = models.CharField()
    detailed_description = models.TextField()
    number = models.CharField()
    media = models.URLField()
    item_id = models.OneToOneField(
        LostItem,
        on_delete=models.CASCADE,
        primary_key=False,
    )