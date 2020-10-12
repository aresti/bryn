import uuid

import pytest

from rest_framework.test import APIClient

from userdb.models import Team, TeamMember, Region


@pytest.fixture
def test_password():
    return "strong-pass"


@pytest.fixture
def region_factory(db):
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
def user_factory(db, django_user_model, test_password):
    def create_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return create_user


@pytest.fixture
def user_a(user_factory):
    return user_factory()


@pytest.fixture
def team_with_admin_factory(db, user_a, region_a):
    def create_team_with_admin(**kwargs):
        if "user" not in kwargs:
            user = user_a
        if "default_region" not in kwargs:
            region = region_a
        defaults = {
            "name": "Test Team",
            "creator": user,
            "position": "PI",
            "department": "Test Department",
            "institution": "Quadram",
            "phone_number": "+441234567123",
            "research_interests": "Testing stuff",
            "intended_climb_use": "Breaking stuff",
            "held_mrc_grants": "CLIMB-BIG-DATA",
            "verified": True,
            "default_region": region,
            "tenants_available": True,
        }
        kwargs = {**defaults, **kwargs}
        team = Team.objects.create(**kwargs)
        TeamMember.objects.create(team=team, user=user, is_admin=True)
        return team, user

    return create_team_with_admin


@pytest.fixture
def team_a(team_with_admin_factory):
    return team_with_admin_factory()


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
