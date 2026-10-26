from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

#manager for user model
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


#models.TextChoices is a helper for defining a fixed set of options for a text field
class Dialect(models.TextChoices):
    PADANG = ("padang", "Padang (Northeastern)")
    RUWENG = ("ruweng", "Ruweng (Northwestern)")
    REK = ("rek", "Rek (Southwestern)")
    AGAR = ("agar", "Agar (Southcentral)")
    BOR = ("bor", "Bor (Southeastern)")



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    dialect = models.CharField(max_length=20, choices=Dialect.choices, blank=True)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
