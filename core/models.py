from django.db import models

# Admin Model
class Admin(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    username = models.CharField(unique=True)
    name = models.CharField()
    password = models.CharField()
    position = models.CharField()

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

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()
    category = models.CharField(max_length=2, choices=Categories.choices, default=Categories.MISC)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.UNCLAIMED)
    description = models.TextField()
    location_found = models.TextField()
    photo_url = models.CharField()

    class Meta:
        db_table = 'LostItem'
        db_table_comment = 'Lost Item Attributes'

# Claim Form Model
class ClaimForm(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_id = models.OneToOneField(
        LostItem,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    name = models.CharField()
    email = models.CharField()
    number = models.CharField()
    media = models.CharField()
    created_at = models.DateTimeField()