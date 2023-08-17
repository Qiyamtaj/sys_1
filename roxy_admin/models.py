"""
Models module for user, volunteer and surfer models
"""

from datetime import date
from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import qrcode
from django.core.files.base import ContentFile
from django.core.files import File
from io import BytesIO

class UserManager(BaseUserManager):
    """
    Manager for custom user model
    """
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a new user with given details
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a new superuser with given details
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom user model
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Volunteer(models.Model):
    """
    Model representing a volunteer.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    id = models.UUIDField( default=uuid.uuid4, editable=False, unique=True, db_index=True , primary_key=True)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    DOB = models.DateField()

    @property
    def age(self):
        today = date.today()
        return today.year - self.DOB.year - ((today.month, today.day) < (self.DOB.month, self.DOB.day))
    
    gender = models.CharField(max_length=100)
    race = models.CharField(max_length=100)
    hours = models.FloatField(default=0.0)
    attendance = models.IntegerField(default=0)
    role = models.CharField(max_length=100)
    medical_issues = models.CharField(max_length=1000)
    occupation = models.CharField(max_length=100)
    offered_services = models.CharField(max_length=1000)
    availablity = models.CharField(max_length=100)
    extra_info = models.CharField(max_length=500)
    swim_longer_than_5_min = models.BooleanField()
    comfortablity_in_ocean = models.CharField(max_length=100)
    previous_volunteer = models.BooleanField()
    emergency_contact_first_name = models.CharField(max_length=100)
    emergency_contact_last_name = models.CharField(max_length=100)
    emergency_contact_cell = models.CharField(max_length=100)
    medical_aid = models.CharField(max_length=100)
    medical_aid_num = models.CharField(max_length=100)
    receive_newsletter = models.CharField(max_length=3)
    accept_TandC = models.CharField(max_length=3)
    qr_code = models.ImageField(upload_to='qrcodes', blank=True)
    is_timing_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(self.id)) # add user's uuid here
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')

            temp_handle = BytesIO()
            img.save(temp_handle, 'PNG')
            temp_handle.seek(0)
            self.qr_code.save(f'{self.id}.png', ContentFile(temp_handle.read()), save=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the volunteer object.
        """
        return f"{self.user.first_name} {self.user.last_name}"


class Surfer(models.Model):
    """Model representing a surfer."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True, primary_key=True)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    DOB = models.DateField()
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.DOB.year - ((today.month, today.day) < (self.DOB.month, self.DOB.day))
    
    onset_of_condition = models.DateField()
    gender = models.CharField(max_length=100)
    race = models.CharField(max_length=100)
    medical_issues = models.CharField(max_length=1000)
    occupation = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    diagnosis_and_needs = models.CharField(max_length=1000)
    hours = models.FloatField(default=0.0)
    attendance = models.IntegerField(default=0)
    role = models.CharField(max_length=100)
    disability = models.CharField(max_length=100)
    medication = models.CharField(max_length=500)
    extra_info = models.CharField(max_length=500)
    swim_longer_than_5_min = models.BooleanField()
    comfortablity_in_ocean = models.CharField(max_length=100)
    emergency_contact_first_name = models.CharField(max_length=100)
    emergency_contact_last_name = models.CharField(max_length=100)
    emergency_contact_cell = models.CharField(max_length=100)
    medical_aid = models.CharField(max_length=100)
    medical_aid_num = models.CharField(max_length=100)
    receive_newsletter = models.CharField(max_length=3)
    accept_TandC = models.CharField(max_length=3)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    is_timing_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(self.id)) # add user's uuid here
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')

            temp_handle = BytesIO()
            img.save(temp_handle, 'PNG')
            temp_handle.seek(0)
            self.qr_code.save(f'{self.id}.png', ContentFile(temp_handle.read()), save=False)
            
        
        super().save(*args, **kwargs)

    def __str__(self):
        """Return string representation of the Surfer object."""
        return f"{self.user.first_name} {self.user.last_name}"


class Event(models.Model):
    """
    Model representing an event.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return string representation of the Event object."""
        return f"{self.title}"




