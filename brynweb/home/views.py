from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from humps import camelize

from openstack.models import Region
from openstack.serializers import RegionSerializer
from userdb.serializers import TeamSerializer, UserSerializer


class ValidatedEmailRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.email_validated:
            return HttpResponseRedirect(reverse("user:email_validation_pending"))
        return super().dispatch(request, *args, **kwargs)


class ActiveTeamRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        teams = request.user.teams.all()
        if len(teams.filter(verified=True)):
            return super().dispatch(request, *args, **kwargs)

        # No active teams
        if not len(teams):
            # No teams whatsoever
            messages.error(request, "You have no current team memberships.")
        else:
            # No active teams
            messages.info(
                request,
                "Your team is pending approval by our team. We'll be in touch soon.",
            )
        return HttpResponseRedirect(reverse("user:login"))


class TeamDashboard(
    LoginRequiredMixin,
    ValidatedEmailRequiredMixin,
    ActiveTeamRequiredMixin,
    TemplateView,
):
    """
    Team dashboard (home)
    """

    template_name = "home/dashboard.html"

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        user_data = camelize(UserSerializer(user).data)
        user_teams = user.teams.all()
        team_data = camelize(TeamSerializer(user_teams, many=True).data)
        region_data = camelize(RegionSerializer(Region.objects.all(), many=True).data)

        return {"regions": region_data, "teams": team_data, "user": user_data}
