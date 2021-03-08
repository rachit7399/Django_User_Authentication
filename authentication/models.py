from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.contrib.auth.models import User
import uuid
from .UserManager import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email   
        
    def tokens(self):
        return ''                
