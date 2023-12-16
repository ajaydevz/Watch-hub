from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager,Group as AuthGroup, Permission as AuthPermission
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

        


class CustomUser(AbstractUser):
  
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20,unique=False,verbose_name='phone number',
                             blank=True,null=True, help_text='enter 10 digit phone number')
    username = models.CharField(max_length=20,unique=False,verbose_name='username',
                             blank=True,null=True,)
    
    wallet  = models.PositiveIntegerField(default=0)
    otp = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        AuthGroup,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_users',
    )
    
    
    # Define a related_name for user_permissions
    user_permissions = models.ManyToManyField(
        AuthPermission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_users',  # Add this line
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    class Meta:
        verbose_name='CustomUser'
        verbose_name_plural="CustomUsers"
    
#USER WALLET MODEL FOR WALLET
class UserWallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()

    def _str_(self):
        return f'{self.user.username} amount {self.amount}'
    