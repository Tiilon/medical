from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string
from django.contrib.auth.models import PermissionsMixin
from base.models import *


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.is_active = True
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        db_table = "user"
        # indexes = [models.Index(fields=['zone']), models.Index(fields=['owner'])]

    def __str__(self):
        return f"{self.email}"

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    @property
    def get_random_password(self):
        return get_random_string(length=6)

    @property
    def get_status(self):
        return "Deactivate" if self.is_active else "Activate"

MARITAL = {
    ('Married', 'Married'),
    ('Single', 'Single'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
}

class UserProfile(BaseModel):
    user = models.OneToOneField(
        User,
        related_name="user_profile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    other_name = models.CharField(max_length=255, null=True, blank=True)
    bio_file = models.FileField(upload_to='user/bio', blank=True, null=True)
    phone = models.CharField(max_length=25, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    email_token = models.CharField(max_length=300, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profession = models.CharField(max_length=255,null=True, blank=True)
    # nationality = models.ForeignKey(Nationality, related_name='nationality', on_delete=models.CASCADE, null=True, blank=True)
    personal_website = models.CharField(max_length=300, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    marital_status = models.CharField(max_length=100,blank=True,null=True,choices=MARITAL)



    # Metadata
    class Meta:
        db_table = "User Profile"

    # Methods
    def __str__(self):
        return f"{self.user}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
