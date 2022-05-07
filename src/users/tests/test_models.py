from django.utils.text import slugify

from faker import Faker
import pytest

from users.models import User

FAKE = Faker("pt_BR")


@pytest.mark.django_db
class TestUserManager:
    def test_create_user(self):
        email = FAKE.email()
        username = slugify(email)
        password = FAKE.name()
        user = User.objects._create_user(email, password)

        assert user.username == username
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_with_raise_exception(self):
        email = FAKE.email()
        password = FAKE.name()

        with pytest.raises(ValueError):
            User.objects._create_user(None, password, username=email)

    def test_create_superuser(self):
        email = FAKE.email()
        password = FAKE.name()
        user = User.objects.create_superuser(email, password)

        assert user.is_staff
        assert user.is_superuser
        assert user.is_active


@pytest.mark.django_db
class TestUserModel:
    def test_user___str__(self, user):
        """Ensure that converting user to string return email"""
        user_email = user.email
        user_str = str(user)

        assert user_str == user_email
