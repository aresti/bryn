import uuid

import pytest

from rest_framework.test import APIClient

from userdb.models import Team, TeamMember, Region, Invitation


@pytest.fixture
def test_password():
    return "strong-pass"


@pytest.fixture
def region_factory():
    def create_region(**kwargs):
        defaults = {
            "name": "Birmingham",
            "description": "Birmingham Region",
            "disabled": False,
            "disable_new_instances": False,
        }
        kwargs = {**defaults, **kwargs}
        return Region.objects.create(**kwargs)

    return create_region


@pytest.fixture
def region_a(region_factory):
    return region_factory()


@pytest.fixture
def user_factory(django_user_model, test_password):
    def create_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return create_user


@pytest.fixture
def teammember_factory(user_factory):
    def create_teammember(team, user=None, is_admin=False):
        if not user:
            user = user_factory()
        return TeamMember.objects.create(team=team, user=user, is_admin=is_admin)

    return create_teammember


@pytest.fixture
def invitation_factory():
    def create_invitation(to_team, **kwargs):
        defaults = {
            "to_team": to_team,
            "made_by": to_team.admin_users.first(),
            "email": f"{uuid.uuid4()}@gmail.com",
            "message": "Join us!",
            "accepted": False,
        }
        kwargs = {**defaults, **kwargs}
        return Invitation.objects.create(**kwargs)

    return create_invitation


@pytest.fixture
def team_factory(user_factory, teammember_factory, invitation_factory, region_a):
    def create_team(extra_members=0, invitations=0, **kwargs):
        if "creator" not in kwargs:
            creator = user_factory()
        if "default_region" not in kwargs:
            default_region = region_a
        defaults = {
            "name": "Test Team",
            "creator": creator,
            "position": "PI",
            "department": "Test Department",
            "institution": "Quadram",
            "phone_number": "+441234567123",
            "research_interests": "Testing stuff",
            "intended_climb_use": "Breaking stuff",
            "held_mrc_grants": "CLIMB-BIG-DATA",
            "verified": True,
            "default_region": default_region,
            "tenants_available": True,
        }
        kwargs = {**defaults, **kwargs}

        # Make creator team admin
        team = Team.objects.create(**kwargs)
        teammember_factory(team, creator, is_admin=True)

        # Add extra team members
        for _ in range(extra_members):
            teammember_factory(team)

        # Add invitations
        for _ in range(invitations):
            invitation_factory(team)

        return team

    return create_team


@pytest.fixture
def team_a(team_factory):
    return team_factory(extra_members=3, invitations=2)


@pytest.fixture
def team_b(team_factory):
    return team_factory(extra_members=3, invitations=2)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_authenticated_api_client(db, api_client):
    def authenticate_api_client(user):
        api_client.force_authenticate(user=user)
        return api_client

    yield authenticate_api_client
    api_client.force_authenticate(user=None)
