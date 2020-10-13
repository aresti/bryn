import pytest

from django.urls import reverse
from rest_framework import status


@pytest.fixture
def teammembers_list_response(team_a, get_authenticated_api_client):
    """
    Return response for GET request to api-teammembers-list
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = client.get(url)
    return response


def test_teammembers_api_allows_authorized_admin(teammembers_list_response,):
    """
    Can an authorized team admin access team api routes?
    """
    assert teammembers_list_response.status_code == status.HTTP_200_OK


def test_teammembers_api_rejects_unauthorized_user(api_client, team_a):
    """
    Are unauthorized users forbidden from accessing team api routes?
    """
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_teammembers_api_rejects_regular_team_member(
    get_authenticated_api_client, team_a
):
    """
    Are regular team members forbidden from accessing team api routes?
    """
    client = get_authenticated_api_client(team_a.regular_users[0])
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_teammembers_api_rejects_different_team_admin(
    get_authenticated_api_client, team_a, team_b
):
    """
    Are admins from other teams forbidden from accessing team api routes?
    """
    client = get_authenticated_api_client(team_b.admin_users[0])
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_teammembers_list_returns_correct_users_for_team(
    teammembers_list_response, team_a
):
    """
    Are the correct users returned by api-teammembers-list?
    """
    response = teammembers_list_response
    assert len(response.data) == team_a.teammember_set.count()
    for member in response.data:
        assert team_a.teammember_set.filter(id__exact=member["id"]).exists()


def test_teammembers_list_response_is_correctly_formatted(
    teammembers_list_response, team_a
):
    """
    Is the response api-teammembers-list correctly formatted?
    """
    response = teammembers_list_response
    response_member = response.data[0]
    member = team_a.teammember_set.get(pk=response_member["id"])
    expected = {
        "id": member.id,
        "user": {
            "username": member.user.username,
            "first_name": member.user.first_name,
            "last_name": member.user.last_name,
        },
        "is_admin": member.is_admin,
    }
    assert response.data[0] == expected
