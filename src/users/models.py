from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from members.models import Member


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        username = slugify(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()

        Member.objects.create(
            name="%s %s" % (user.first_name, user.last_name),
            user=user,
        )

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        "Endereço de E-mail",
        error_messages={
            "unique": "A user with that e-mail already exists.",
        },
        unique=True,
    )
    last_name = models.CharField("Sobrenome", max_length=128)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        ordering = ("-id",)
        verbose_name = "Usuário"

    def __str__(self) -> str:
        return str(self.email)
