from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.timezone import now
from datetime import datetime
import pyotp
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, email, mobile, password=None, **extra_fields):
        
        if not email and mobile:
            raise ValueError('Users must have an email or mobile')

        account = self.model(
            email=self.normalize_email(email),
            mobile=mobile,

        )
        account.account_type = extra_fields.get('account_type')
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, email, password, mobile, **extra_fields):
        
        account = self.create_user(
            email,
            mobile,
            password=password,
        )
        account.account_type = 'S'
        account.is_admin = True
        account.save(using=self._db)
        return account

class Account(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )
    type_choice = (('S', 'Super Admin'),
                   ('A', 'Admin'),
                   ('U','User'),
                   )
    account_type = models.CharField(choices=type_choice, max_length=1, null=True)
    mobile = models.CharField(max_length=15,unique=True,)
    name = models.CharField(max_length=40, null=True,blank=False)
    image = models.URLField(max_length=540,blank=True,null=True)
    otp = models.CharField('OTP', max_length=4, blank=True, null=True)
    otp_verified = models.BooleanField("OTP Verified", default=False)
    email_verified = models.BooleanField("Email Verified", default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'mobile'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return  str(self.mobile+"---->"+self.account_type)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
         return True

    @property
    def is_staff(self):
        return self.is_admin

    def otp_creation(self):
        '''Otp creation with 4 digits'''
        totp = pyotp.TOTP("JBSWY3DPEHPK3PXP", digits=4)
        otp = totp.now()
        self.otp = otp
        self.save()
        print(otp)
        return otp

    def otp_send(self,otp,to):
        '''Function for sending otp'''
        try:
            # message = settings.SMS_CLIENT.messages.create(
            #     body="OTP is "+otp,
            #     from_='+16029753620',
            #     to=to)
            return True
        except Exception as e:
            print("Exception",e)
            return False

    def otp_verification(self, otp):
        ''' Otp verify '''
        if self.otp == otp:
            self.otp_creation()
            return True
        return False


class Trackable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Account, related_name='created_%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(Account, related_name='updated_%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField('Active', default=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True
