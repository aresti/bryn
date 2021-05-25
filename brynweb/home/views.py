from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from userdb.models import Invitation, LicenceVersion


class FrontendView(LoginRequiredMixin, TemplateView):
    """
    Frontend View: render Vue SPA
    """

    template_name = "home/index.html"

    def get_context_data(self, *args, **kwargs):
        try:
            licence_terms = LicenceVersion.objects.current().licence_terms
        except LicenceVersion.DoesNotExist:
            licence_terms = None

        return {
            "licence_terms": licence_terms,
        }

    def dispatch(self, request, *args, **kwargs):
        """Handle case where user logs in with no team, but pending invite"""
        if request.user.is_authenticated:
            has_teams = bool(request.user.teams.count())
            has_pending_invitations = bool(
                Invitation.objects.filter(
                    email=request.user.email, accepted=False
                ).count()
            )
            if not has_teams and has_pending_invitations:
                messages.error(
                    request,
                    "You have no current team memberships. If you have received a team invitation, please follow the "
                    "email link to accept.",
                )
                return redirect("user:logout")

        return super().dispatch(request, *args, **kwargs)
