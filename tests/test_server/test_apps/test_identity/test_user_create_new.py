from typing import Any

import pytest

from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
)
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew
from server.apps.identity.models import User
from server.common.django.types import Settings
from tests.plugins.identity.user import (
    UserAssertion,
    RegistrationData,
    NotLeadUserAssertion,
)

pytestmark = pytest.mark.django_db


@pytest.mark.slow()
def test_success_create_new_user(
    user: User,
    settings: Settings,
    assert_correct_user: UserAssertion,
    assert_not_lead_user: NotLeadUserAssertion,
    reg_data: RegistrationData,
    expected_user_data: dict[str, Any],
) -> None:
    """Testing usecase that create new user."""
    assert_correct_user(reg_data['email'], expected_user_data)
    assert_not_lead_user(reg_data['email'])

    UserCreateNew(settings=settings)(user=user)
    user.refresh_from_db()
    assert user.lead_id is not None


def test_success_update_user_ids(
    user: User,
    settings: Settings,
    assert_correct_user: UserAssertion,
    reg_data: RegistrationData,
    expected_user_data: dict[str, Any],
) -> None:
    """Testing usecase that update user id."""
    assert_correct_user(reg_data['email'], expected_user_data)
    response = UserResponse(id=100)
    UserCreateNew(settings=settings)._update_user_ids(  # noqa: WPS437
        user=user, response=response,
    )
    actual_user = User.objects.get(email=reg_data['email'])
    assert actual_user.lead_id == response.id
