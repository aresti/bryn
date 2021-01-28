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

    def test_invitation_list_allows_retrieve_create(self):
        self.client.force_login(user=self.team_b_admin)
        response = self.client.head(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        allow = response["Allow"]
        self.assertEqual(allow, "GET, POST, HEAD, OPTIONS")

    def test_anon_user_cannot_get_invitation_list(self):
        """Are non-authenticated users forbidden from list endpoint?"""
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_member_can_create_invitation(self):
        """Can team admins create invitations?"""
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
        """Can team admins view invitations?"""
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_admin)
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_admin_from_another_team_cannot_view_invitations(self):
        """Are team admins restricted to only seeing their own invitations?"""
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_b_admin)
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_view_invitations(self):
        """Is a non-admin team member forbidden from viewing invitations?"""
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_member1)
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invitiations_list_only_shows_correct_team(self):
        """Does the invitations list only show teams for the team specified in the url?"""
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        InvitationFactory(to_team=self.team_b, made_by=self.team_b_admin)
        InvitationFactory(to_team=self.team_b, made_by=self.team_b_admin)
        self.client.force_login(user=self.team_a_admin)
        response = self.client.get(
            reverse(self.path_name, kwargs={"team_id": self.team_a.pk})
        )
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("to_team"), self.team_a.hashid)

    def test_non_admin_cannot_create_invitation(self):
        """Are non-amdmin team members forbidden from creating invitations?"""
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
        """Are non-authorised users forbidden from viewing individual invitations?"""
        invitation = InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        response = self.client.get(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_member_can_get_invitation_detail(self):
        """Can team admins view individual invitations?"""
        invitation = InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_admin)
        response = self.client.get(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("uuid"), str(invitation.uuid))

    def test_non_admin_member_cannot_get_invitation_detail(self):
        """Are non-admin team members forbidden from viewing individual invitations?"""
        invitation = InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_member1)
        response = self.client.get(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_delete_an_invitation(self):
        """Can a team admin delete an invitation?"""
        invitation = InvitationFactory(to_team=self.team_a, made_by=self.team_a_admin)
        self.client.force_login(user=self.team_a_admin)
        response = self.client.delete(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invitation.objects.count(), 0)

    def test_cannot_delete_an_accepted_invitation(self):
        """Is delete prevented for accepted invitations"""
        invitation = InvitationFactory(
            to_team=self.team_a, made_by=self.team_a_admin, accepted=True
        )
        self.client.force_login(user=self.team_a_admin)
        response = self.client.delete(
            reverse(
                self.path_name, kwargs={"team_id": self.team_a.pk, "pk": invitation.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertContains(
            response, "Accepted invitations cannot be deleted", status_code=405
        )


class TestUserProfileAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Shared setup
        cls.path_name = "api:user_profile"

        cls.user_a = UserFactory()
        cls.user_b = UserFactory()

    def test_anon_user_cannot_view_user_profile(self):
        """Are non-authenticated users forbidden from user profile endpoint?"""
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile_endpoint_returns_logged_in_user(self):
        """Does the user profile return the logged in user?"""
        self.client.force_login(user=self.user_a)
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.data.get("username"), self.user_a.username)

    def test_user_can_update_profile(self):
        """Can the logged in user update his profile?"""
        self.client.force_login(user=self.user_a)
        response = self.client.patch(
            reverse(self.path_name), data={"first_name": "Jim"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user_a.pk).first_name, "Jim")

    def test_updating_email_sets_email_validated_false(self):
        self.user_a.profile.email_validated = True
        self.client.force_login(user=self.user_a)
        self.client.patch(reverse(self.path_name), data={"email": "something@new.com"})
        updated_user = User.objects.get(pk=self.user_a.pk)
        self.assertEqual(updated_user.profile.email_validated, False)
