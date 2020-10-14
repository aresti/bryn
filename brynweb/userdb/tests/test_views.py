import pytest
import uuid

from django.urls import reverse
from rest_framework import status

from userdb.serializers import InvitationSerializer, TeamMemberSerializer


@pytest.fixture
def team_a_regular_member(team_a):
    return team_a.teammember_set.filter(is_admin=False).first()


@pytest.fixture
def team_a_admin_member(team_a):
    return team_a.teammember_set.filter(is_admin=True).first()


@pytest.fixture
def teammembers_list_url_team_a(team_a):
    """
    Return a url for api-teammember-list, for team_a
    """
    return reverse("user:api-teammember-list", kwargs={"team_id": team_a.pk})


@pytest.fixture
def teammembers_detail_url_team_a(team_a, team_a_regular_member):
    """
    Return a url for api-teammember-detail, for a team member in team_a
    """
    return reverse(
        "user:api-teammember-detail",
        kwargs={"team_id": team_a.pk, "pk": team_a_regular_member.id},
    )


@pytest.fixture
def invitation_detail_url_team_a(team_a):
    """
    Return a url for api-invitation-detail, for team_a
    """
    return reverse(
        "user:api-invitation-detail",
        kwargs={"team_id": team_a.pk, "pk": team_a.invitations.first().pk},
    )


@pytest.fixture
def invitation_list_url_team_a(team_a):
    """
    Return a url for api-invitation-list, for team_a
    """
    return reverse("user:api-invitation-list", kwargs={"team_id": team_a.pk})


@pytest.fixture
def teammember_list_get_response(
    team_a, get_authenticated_api_client, teammembers_list_url_team_a
):
    """
    Return response for GET request to api-teammember-list
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(teammembers_list_url_team_a)
    return response


@pytest.fixture
def teammember_detail_get_response(
    team_a, get_authenticated_api_client, teammembers_detail_url_team_a
):
    """
    Return response for GET request to api-teammember-detail
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(teammembers_detail_url_team_a)
    return response


@pytest.fixture
def invitation_detail_get_response(
    team_a, get_authenticated_api_client, invitation_detail_url_team_a
):
    """
    Return response for GET request to api-teammember-detail
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(invitation_detail_url_team_a)
    return response


@pytest.fixture
def invitation_list_get_response(
    team_a, get_authenticated_api_client, invitation_list_url_team_a
):
    """
    Return response for GET request to api-teammember-list
    by authorized team admin.
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(invitation_list_url_team_a)
    return response


@pytest.mark.parametrize(
    "response",
    [
        pytest.lazy_fixture("teammember_list_get_response"),
        pytest.lazy_fixture("teammember_detail_get_response"),
        pytest.lazy_fixture("invitation_list_get_response"),
        pytest.lazy_fixture("invitation_detail_get_response"),
    ],
)
def test_teammember_api_allows_authorized_admin(response,):
    """
    Can an authorized team admin access team api routes (GET)?
    """
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "url",
    [
        pytest.lazy_fixture("teammembers_list_url_team_a"),
        pytest.lazy_fixture("teammembers_detail_url_team_a"),
        pytest.lazy_fixture("invitation_list_url_team_a"),
        pytest.lazy_fixture("invitation_detail_url_team_a"),
    ],
)
def test_teammember_api_rejects_unauthorized_user(api_client, url):
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
        pytest.lazy_fixture("invitation_list_url_team_a"),
        pytest.lazy_fixture("invitation_detail_url_team_a"),
    ],
)
def test_teammember_api_rejects_regular_team_member_get(
    get_authenticated_api_client, team_a, url
):
    """
    Are regular team members forbidden from accessing team api routes (GET)?
    """
    client = get_authenticated_api_client(team_a.regular_users[0])
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "url",
    [
        pytest.lazy_fixture("teammembers_list_url_team_a"),
        pytest.lazy_fixture("teammembers_detail_url_team_a"),
        pytest.lazy_fixture("invitation_list_url_team_a"),
        pytest.lazy_fixture("invitation_detail_url_team_a"),
    ],
)
def test_teammember_api_rejects_regular_team_member_delete(
    get_authenticated_api_client, team_a, url
):
    """
    Are regular team members forbidden from accessing team api routes (DELETE)?
    """
    client = get_authenticated_api_client(team_a.regular_users[0])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "url",
    [
        pytest.lazy_fixture("teammembers_list_url_team_a"),
        pytest.lazy_fixture("teammembers_detail_url_team_a"),
        pytest.lazy_fixture("invitation_list_url_team_a"),
        pytest.lazy_fixture("invitation_detail_url_team_a"),
    ],
)
def test_teammember_api_rejects_different_team_admin(
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
        reverse("user:api-teammember-list", kwargs={"team_id": 12345}),
        reverse("user:api-teammember-detail", kwargs={"team_id": 1, "pk": 9999}),
        reverse("user:api-invitation-list", kwargs={"team_id": 12345}),
        reverse(
            "user:api-invitation-detail", kwargs={"team_id": 1, "pk": uuid.uuid4()}
        ),
    ],
)
def test_teammember_list_returns_404_for_missing_team(
    get_authenticated_api_client, team_a, url
):
    """
    Do api-teammembers views return 404 for a missing resource?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_teammember_list_returns_correct_users_for_team(
    teammember_list_get_response, team_a
):
    """
    Are the correct users returned by api-teammember-list?
    """
    response = teammember_list_get_response
    assert len(response.data) == team_a.teammember_set.count()
    for member in response.data:
        assert team_a.teammember_set.filter(id__exact=member["id"]).exists()


def test_teammember_list_get_response_correctly_formatted(
    teammember_list_get_response, team_a
):
    """
    Is the response data for api-teammember-list as expected?
    """
    response = teammember_list_get_response
    expected = TeamMemberSerializer(team_a.teammember_set.all(), many=True).data
    assert response.data == expected


def test_teammember_detail_get_response_correctly_formatted(
    get_authenticated_api_client, team_a, team_a_regular_member
):
    """
    Is the response data for api-teammember-detail GET as expected?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    url = reverse(
        "user:api-teammember-detail",
        kwargs={"team_id": team_a.pk, "pk": team_a_regular_member.id},
    )
    response = client.get(url)
    expected = TeamMemberSerializer(team_a_regular_member).data
    assert response.data == expected


def test_teammember_detail_admin_can_delete(
    get_authenticated_api_client, team_a, team_a_regular_member
):
    """
    Can a team admin delete a regular member?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    url = reverse(
        "user:api-teammember-detail",
        kwargs={"team_id": team_a.pk, "pk": team_a_regular_member.id},
    )
    initial_member_count = team_a.teammember_set.count()
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert team_a.teammember_set.count() == initial_member_count - 1


def test_teammember_detail_delete_own_membership_forbidden(
    get_authenticated_api_client, team_a, team_a_admin_member
):
    """
    Is deleting a your own membership forbidden, even for an authorized admin?
    """
    own_membership = team_a_admin_member
    client = get_authenticated_api_client(own_membership.user)
    url = reverse(
        "user:api-teammember-detail",
        kwargs={"team_id": team_a.pk, "pk": own_membership.id},
    )
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_teammember_detail_delete_extra_admin_allowed(
    get_authenticated_api_client, team_a, teammember_factory
):
    """
    Is DELETE allowed for 'extra' team admins?
    """
    user = team_a.admin_users.first()
    extra_admin_member = teammember_factory(team_a, is_admin=True)
    client = get_authenticated_api_client(user)
    url = reverse(
        "user:api-teammember-detail",
        kwargs={"team_id": team_a.pk, "pk": extra_admin_member.id},
    )
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_invitation_list_returns_correct_invitations_for_team(
    invitation_list_get_response, team_a
):
    """
    Are the correct invitations returned by api-invitation-list GET?
    """
    response = invitation_list_get_response
    assert len(response.data) == team_a.invitations.count()
    for invitation in response.data:
        assert team_a.invitations.filter(uuid__exact=invitation["uuid"]).exists()


def test_invitation_list_get_response_correctly_formatted(
    invitation_list_get_response, team_a
):
    """
    Is the response data for api-invitation-list GET as expected?
    """
    response = invitation_list_get_response
    expected = InvitationSerializer(team_a.invitations.all(), many=True).data
    assert response.data == expected


def test_invitation_detail_get_response_correctly_formatted(
    get_authenticated_api_client, team_a
):
    """
    Is the response data for api-invitation-detail GET as expected?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    invitation = team_a.invitations.first()
    url = reverse(
        "user:api-invitation-detail",
        kwargs={"team_id": team_a.pk, "pk": invitation.pk},
    )
    response = client.get(url)
    expected = InvitationSerializer(invitation).data
    assert response.data == expected


def test_invitation_detail_admin_can_delete(get_authenticated_api_client, team_a):
    """
    Can a team admin delete an invitation?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    invitation = team_a.invitations.first()
    url = reverse(
        "user:api-invitation-detail",
        kwargs={"team_id": team_a.pk, "pk": invitation.pk},
    )
    initial_invitation_count = team_a.invitations.count()
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert team_a.invitations.count() == initial_invitation_count - 1


def test_invitation_list_admin_can_post(
    get_authenticated_api_client, invitation_list_url_team_a, team_a
):
    """
    Can a team admin create an invitation?
    """
    client = get_authenticated_api_client(team_a.admin_users[0])
    post_data = {"email": f"{uuid.uuid4()}@gmail.com", "message": "Join us!"}
    initial_invitation_count = team_a.invitations.count()
    response = client.post(invitation_list_url_team_a, post_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert team_a.invitations.count() == initial_invitation_count + 1
