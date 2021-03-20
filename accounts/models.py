from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken
from utils.models import TimestampedModel


class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **kwargs):
        """ create new user """
        if not mobile:
            raise ValueError("User Must have mobile")
        user = self.model(mobile=mobile, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        user = self.create_user(mobile=mobile, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ custom user model using email  """
    mobile = models.CharField(max_length=11, unique=True, validators=[RegexValidator(regex='^01[0|1|2|5][0-9]{8}$',
                                                                                     message="Phone number must be : 010 or 011 or 012 or 015.",
                                                                                     code="Invalid Phone Number")])
    name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }


class PhoneOtp(TimestampedModel):
    otp = models.CharField(max_length=4, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_otp')

    def __str__(self):
        return self.user
