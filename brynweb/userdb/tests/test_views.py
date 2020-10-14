import pytest

from django.urls import reverse
from rest_framework import status

from userdb.serializers import TeamMemberSerializer


@pytest.fixture
def team_a_regular_member(team_a):
    return team_a.teammember_set.filter(is_admin=False).first()


@pytest.fixture
def team_a_admin_member(team_a):
    return team_a.teammember_set.filter(is_admin=True).first()


@pytest.fixture
def teammembers_list_url_team_a(team_a):
    """
    Return a url for api-teammembers-list, for team_a
    """
    return reverse("user:api-teammembers-list", kwargs={"team_id": team_a.pk})


@pytest.fixture
def teammembers_detail_url_team_a(team_a, team_a_regular_member):
    """
    Return a url for api-teammembers-detail, for a team member in team_a
    """
    return reverse(
        "user:api-teammembers-detail",
        kwargs={"team_id": team_a.pk, "pk": team_a_regular_member.id},
    )


@pytest.fixture
def teammembers_list_response(
    team_a, get_authenticated_api_client, teammembers_list_url_team_a
):
    """
    Return response for GET request to api-teammembers-list
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(teammembers_list_url_team_a)
    return response


@pytest.fixture
def teammembers_detail_get_response(
    team_a, get_authenticated_api_client, teammembers_detail_url_team_a
):
    """
    Return response for GET request to api-teammembers-detail
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(teammembers_detail_url_team_a)
    return response


@pytest.mark.parametrize(
    "response",
    [
        pytest.lazy_fixture("teammembers_list_response"),
        pytest.lazy_fixture("teammembers_detail_get_response"),
    ],
)
def test_teammembers_api_allows_authorized_admin(response,):
    """
    Can an authorized team admin access team api routes?
    """
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "url",
    [
        pytest.lazy_fixture("teammembers_list_url_team_a"),
        pytest.lazy_fixture("teammembers_detail_url_team_a"),
    ],
)
def test_teammembers_api_rejects_unauthorized_user(api_client, url):
    """
    Are unauthorized users forbidden from accessing team api routes?
    """
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "url",
    [
        pytest.lazy_fixture("teammembers_list_url_team_a"),
        pytest.lazy_fixture("teammembers_detail_url_team_a"),
    ],
)
def test_teammembers_api_rejects_regular_team_member(
    get_authenticated_api_client, team_a, url
):
    """
    Are regular team members forbidden from accessing team api routes?
    """
    client = get_authenticated_api_client(team_a.regular_users[0])
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "url",
    [
        pytest.lazy_fixture("teammembers_list_url_team_a"),
        pytest.lazy_fixture("teammembers_detail_url_team_a"),
    ],
)
def test_teammembers_api_rejects_different_team_admin(
    get_authenticated_api_client, team_b, url
):
    """
    Are admins from other teams forbidden from accessing team api routes?
    """
    client = get_authenticated_api_client(team_b.admin_users[0])
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "url",
    [
        reverse("user:api-teammembers-list", kwargs={"team_id": 12345}),
        reverse("user:api-teammembers-detail", kwargs={"team_id": 1, "pk": 9999}),
    ],
)
def test_teammembers_list_returns_404_for_missing_team(
    get_authenticated_api_client, team_a, url
):
    """
    Do api-teammembers views return 404 for a missing resource?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


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


def test_teammembers_list_response_correctly_formatted(
    teammembers_list_response, team_a
):
    """
    Is the response data for api-teammembers-list as expected?
    """
    response = teammembers_list_response
    expected = TeamMemberSerializer(team_a.teammember_set.all(), many=True).data
    assert response.data == expected


def test_teammembers_detail_get_response_correctly_formatted(
    get_authenticated_api_client, team_a, team_a_regular_member
):
    """
    Is the response data for api-teammembers-detail GET as expected?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    url = reverse(
        "user:api-teammembers-detail",
        kwargs={"team_id": team_a.pk, "pk": team_a_regular_member.id},
    )
    response = client.get(url)
    expected = TeamMemberSerializer(team_a_regular_member).data
    assert response.data == expected


def test_teammembers_detail_admin_can_delete(
    get_authenticated_api_client, team_a, team_a_regular_member
):
    """
    Can a team admin delete a regular member?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    url = reverse(
        "user:api-teammembers-detail",
        kwargs={"team_id": team_a.pk, "pk": team_a_regular_member.id},
    )
    initial_member_count = team_a.teammember_set.count()
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert team_a.teammember_set.count() == initial_member_count - 1


def test_teammembers_detail_delete_own_membership_forbidden(
    get_authenticated_api_client, team_a, team_a_admin_member
):
    """
    Is deleting a your own membership forbidden, even for an authorized admin?
    """
    own_membership = team_a_admin_member
    client = get_authenticated_api_client(own_membership.user)
    url = reverse(
        "user:api-teammembers-detail",
        kwargs={"team_id": team_a.pk, "pk": own_membership.id},
    )
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_teammembers_detail_delete_extra_admin_allowed(
    get_authenticated_api_client, team_a, teammember_factory
):
    """
    Is deleting an 'extra' team admin allowed?
    """
    user = team_a.admin_users.first()
    extra_admin_member = teammember_factory(team_a, is_admin=True)
    client = get_authenticated_api_client(user)
    url = reverse(
        "user:api-teammembers-detail",
        kwargs={"team_id": team_a.pk, "pk": extra_admin_member.id},
    )
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
