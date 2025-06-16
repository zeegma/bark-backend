from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom User Manager
class AdminManager(BaseUserManager):
    def create_user(self, email, name, number, password=None):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            number=number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, number, password=None):
        user = self.create_user(
            email=email,
            name=name,
            number=number,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Admin Model
class Admin(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15, blank=True, null=True)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'number']
    
    objects = AdminManager()
    
    class Meta:
        db_table = 'Admin'
        db_table_comment = 'Admin credentials for secure access.'

# Lost Item Model
class LostItem(models.Model):
    
    # Categories for user to select
    class Categories(models.TextChoices):
        # Used to organize choices for category attribute
        BAGS = 'BA', 'Bags & Backpacks'
        ELECTRONICS = 'EL', 'Electronics'
        EYEWEAR = 'EW', 'Eyewear'
        FOOTWEAR = 'FW', 'Footwear'
        ID = 'ID', 'IDs & Cards'
        KEYS = 'KY', 'Keys'
        MISC = 'MS', 'Miscellaneous'
        MOBILE = 'MB', 'Mobile Devices'
        WALLETS = 'WT', 'Wallets & Purses'
        WATCHES = 'WH', 'Watches & Jewerly'

    # Status for user Eto select
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
    accepted_claim = models.OneToOneField(
        'ClaimForm', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='accepted_claim'
    )

    class Meta:
        db_table = 'LostItem'
        db_table_comment = 'Lost Item Attributes'

# Claim Form Model
class ClaimForm(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_date = models.DateField()
    name = models.CharField(max_length=100)
    ownership_photo = models.CharField()
    detailed_description = models.TextField()
    number = models.CharField(max_length=11)
    media = models.URLField()
    item_id = models.ForeignKey(
        LostItem,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name='claims'
    )

    class Meta:
        db_table = 'ClaimForm'
        db_table_comment = 'Claim Form Attributes'