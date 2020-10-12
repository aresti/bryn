from django.urls import reverse_lazy, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "user"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="userdb/login.html",),
        name="login",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="userdb/password_reset_form.html",
            email_template_name="userdb/email/password_reset_email.txt",
            html_email_template_name="userdb/email/password_reset_email.html",
            subject_template_name="userdb/email/password_reset_subject.txt",
            success_url=reverse_lazy("user:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="userdb/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        r"reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="userdb/password_reset_confirm.html",
            success_url=reverse_lazy("user:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="userdb/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("register/", views.register, name="register"),
    path("invite/", views.invite, name="invite"),
    path("accept-invite/<uuid:uuid>", views.accept_invite, name="accept-invite"),
    path("validate-email/<uuid:uuid>", views.validate_email, name="validate-email"),
    path(
        "institutions/typeahead/",
        views.institution_typeahead,
        name="institution_typeahead",
    ),
    path(
        "api/teams/<int:team_id>/members/<int:pk>",
        views.TeamMemberDetailView.as_view(),
        name="api-teammembers-detail",
    ),
    path(
        "api/teams/<int:team_id>/members/",
        views.TeamMemberListView.as_view(),
        name="api-teammembers-list",
    ),
    path(
        "api/teams/<int:team_id>/invitations/",
        views.InvitationListView.as_view(),
        name="api-invitation-list",
    ),
]
