from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.html import format_html


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            full_name=full_name,

            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    image = models.ImageField(default='user/image/default_user.jpg', upload_to='user/image')
    full_name = models.CharField(max_length=35, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="50px" height="50px">')

    show_image.short_description = 'image'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=20)
    randcode = models.CharField(max_length=5)
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    email_user = models.EmailField(max_length=255)
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email_user
