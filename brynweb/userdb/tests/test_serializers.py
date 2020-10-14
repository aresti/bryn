import pytest

from django.urls import reverse, resolve
from rest_framework.test import APIRequestFactory

from userdb.serializers import (
    InvitationSerializer,
    TeamMemberSerializer,
    UserSerializer,
)


@pytest.fixture
def teammember_serializer_instance(team_a):
    return TeamMemberSerializer(instance=team_a.teammember_set.all()[0])


@pytest.fixture
def user_serializer_instance(team_a):
    return UserSerializer(instance=team_a.creator)


@pytest.fixture
def invitation_serializer_instance(team_a):
    return InvitationSerializer(team_a.invitations.first())


@pytest.mark.parametrize(
    "serializer_instance,expected",
    [
        (
            pytest.lazy_fixture("invitation_serializer_instance"),
            ["uuid", "email", "date", "message"],
        ),
        (
            pytest.lazy_fixture("teammember_serializer_instance"),
            ["id", "user", "is_admin"],
        ),
        (
            pytest.lazy_fixture("user_serializer_instance"),
            ["id", "username", "first_name", "last_name"],
        ),
    ],
)
def test_serializer_has_expected_fields(serializer_instance, expected):
    """
    Does the serializer return the expected fields?
    """
    data = serializer_instance.data
    assert set(data.keys()) == set(expected)


@pytest.fixture
def invitation_context_team_a(team_a):
    """
    Create a context (with request), necessary to test InvitationSerializer
    """
    team_id = team_a.id
    user = team_a.admin_users.first()
    factory = APIRequestFactory()
    url = reverse("user:api-invitation-list", kwargs={"team_id": team_id})
    request = factory.get(url)
    resolver_match = resolve(url)
    request.user = user
    request.resolver_match = resolver_match
    return {"request": request}


def test_invitation_serializer_enforces_unique_invites(
    team_a, invitation_context_team_a
):
    """
    Does the InvitationSerializer enforce unique invites?
    """
    # Need context, since serializer uses CurrentUserDefault() & TeamFromUrlDefault()
    first = InvitationSerializer(team_a.invitations.first())
    second = InvitationSerializer(data=first.data, context=invitation_context_team_a)
    assert not second.is_valid()
    assert second.errors["non_field_errors"][0].code == "unique"


def test_invitation_serializer_gets_to_team_from_url(
    invitation_factory, invitation_context_team_a, team_a, team_b
):
    """
    Does InvitationSerializer set hidden field to_team from url?
    """
    # Create an invite for team b to get some test data
    team_b_serializer = InvitationSerializer(invitation_factory(to_team=team_b))

    # Create a new serializer instance with this data, but context with team_a in url
    team_a_serializer = InvitationSerializer(
        data=team_b_serializer.data, context=invitation_context_team_a
    )
    team_a_serializer.is_valid()
    instance = team_a_serializer.save()

    # New instance should belong to team_a
    assert instance.to_team == team_a
