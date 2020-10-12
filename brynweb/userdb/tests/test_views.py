import pytest

from django.urls import reverse


@pytest.fixture
def team_members_list_get_authorized_admin(team_a, get_authenticated_api_client):
    """
    Return response for GET request to api-teammembers-list
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = client.get(url)
    return response


def test_teammembers_list_get_allows_authorized_admin(
    team_members_list_get_authorized_admin,
):
    """
    Can an authorized team admin access api-teammembers-list?
    """
    response = team_members_list_get_authorized_admin
    assert response.status_code == 200


def test_teammembers_list_get_rejects_unauthorized_user(api_client, team_a):
    """
    Are unauthorized users forbidden from accessing api-teammembers-list?
    """
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = api_client.get(url)
    assert response.status_code == 403


def test_teammembers_list_get_rejects_regular_team_member(
    get_authenticated_api_client, team_a
):
    """
    Are regular team members forbidden from accessing api-teammembers-list?
    """
    client = get_authenticated_api_client(team_a.regular_users[0])
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = client.get(url)
    assert response.status_code == 403


def test_teammembers_list_get_rejects_different_team_admin(
    get_authenticated_api_client, team_a, team_b
):
    """
    Are admins from other teams forbidden from accessing api-teammembers-list?
    """
    client = get_authenticated_api_client(team_b.admin_users[0])
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = client.get(url)
    assert response.status_code == 403
