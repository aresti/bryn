from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .factories import InvitationFactory, TeamFactory, UserFactory
from ..models import Invitation, TeamMember

User = get_user_model()


class TestInvitationAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Shared setup
        cls.path_name = "api:invitations"

        cls.team_a = TeamFactory()
        cls.team_a_admin = UserFactory()
        cls.team_a_member1 = UserFactory()
        TeamMember.objects.create(team=cls.team_a, user=cls.team_a_admin, is_admin=True)
        TeamMember.objects.create(team=cls.team_a, user=cls.team_a_member1)

        cls.team_b = TeamFactory()
        cls.team_b_admin = UserFactory()
        TeamMember.objects.create(team=cls.team_b, user=cls.team_b_admin, is_admin=True)

    def setUp(self):
        # Per method setup
        pass

    def test_anon_user_cannot_get_invitation_list(self):
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_member_can_create_invitation(self):
        self.client.force_login(user=self.team_a_admin)
        data = {
            "to_team": self.team_a.hashid,
            "email": "someonenew@gmail.com",
            "message": "join us!",
        }
        response = self.client.post(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_admin_member_can_view_invitations(self):
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_admin)
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_admin_from_another_team_cannot_view_invitations(self):
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_b_admin)
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_view_invitations(self):
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_member1)
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_create_invitation(self):
        self.client.force_login(user=self.team_a_member1)
        data = {
            "to_team": self.team_a.hashid,
            "email": "someonenew@gmail.com",
            "message": "join us!",
        }
        response = self.client.post(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anon_user_cannot_get_invitation_detail(self):
        invitation = InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        response = self.client.get(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_member_can_get_invitation_detail(self):
        invitation = InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_admin)
        response = self.client.get(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("uuid"), str(invitation.uuid))

    def test_non_admin_member_can_get_invitation_detail(self):
        invitation = InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_member1)
        response = self.client.get(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
