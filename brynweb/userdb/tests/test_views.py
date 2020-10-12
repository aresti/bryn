import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_team_members_list_api_get(team_a, get_authenticated_api_client):
    team, user = team_a
    client = get_authenticated_api_client(user)
    url = reverse("user:api-teammembers-list", kwargs={"team_id": team.pk})
    response = client.get(url)
    assert response.status_code == 200
