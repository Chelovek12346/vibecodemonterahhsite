from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        if not username:
            raise ValueError("Логин обязателен")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
        error_messages={"unique": "Пользователь с таким логином уже существует."},
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        error_messages={"unique": "Пользователь с таким email уже существует."},
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    school = models.CharField(max_length=255, verbose_name="Школа")
    grade = models.PositiveSmallIntegerField(
        verbose_name="Класс",
        validators=[MinValueValidator(1), MaxValueValidator(11)],
    )
    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="GPA",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "school", "grade", "gpa"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
