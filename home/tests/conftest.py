import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


USERNAME = "jos"
PASSWORD = "secret"


@pytest.fixture
def admin_user(db):
    user = get_user_model().objects.create_user(
        username=USERNAME,
        password=PASSWORD,
        is_active=True,
        email="jos-admin@example.com",
    )
    permission = Permission.objects.get(name="Can access Wagtail admin")
    user.user_permissions.add(permission)
    return user