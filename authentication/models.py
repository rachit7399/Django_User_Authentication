from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.contrib.auth.models import User
import uuid

# Create your models here.
class UserManager(BaseUserManager):


    def create_user(self, uid, email, password=None):
        if email is None:
            raise TypeError('Users should have a Email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.uid = uid
        user.save()
        return user   

    def create_superuser(self, uid, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(uid, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user 


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
