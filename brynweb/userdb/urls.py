from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "user"

urlpatterns = [
    # Auth routes
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.logout_then_login, name="logout"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        r"reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Registration
    path("register/", views.RegistrationScreeningView.as_view(), name="register",),
    path("register/team/", views.team_registration_view, name="register_team"),
    path(
        "register/team/done/",
        views.TeamRegistrationDoneView.as_view(),
        name="register_team_done",
    ),
    path(
        "email-validation-pending",
        views.EmailValidationPendingView.as_view(),
        name="email_validation_pending",
    ),
    path(
        "email-validation-send",
        views.EmailValidationSendView.as_view(),
        name="email_validation_send",
    ),
    path(
        "email-validation-sent",
        views.EmailValidationSentView.as_view(),
        name="email_validation_sent",
    ),
    path("accept-invite/<uuid:uuid>", views.accept_invite, name="accept-invite"),
    path(
        "validate-email/<uuid:uuid>",
        views.EmailValidationConfirmView.as_view(),
        name="validate_email",
    ),
    # API
    path("api/teams/<int:pk>", views.TeamDetailView.as_view(), name="api-team-detail",),
    path(
        "api/teammembers/<int:pk>",
        views.TeamMemberDetailView.as_view(),
        name="api-teammember-detail",
    ),
    path(
        "api/teammembers/",
        views.TeamMemberListView.as_view(),
        name="api-teammember-list",
    ),
    path(
        "api/invitations/<uuid:pk>",
        views.InvitationDetailView.as_view(),
        name="api-invitation-detail",
    ),
    path(
        "api/invitations/",
        views.InvitationListView.as_view(),
        name="api-invitation-list",
    ),
    path(
        "api/userprofile/",
        views.OwnUserDetailView.as_view(),
        name="api-ownuser-detail",
    ),
]
