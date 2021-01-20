from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from humps import camelize

from openstack.models import Region
from openstack.serializers import RegionSerializer
from userdb.serializers import TeamSerializer, UserSerializer


class TeamDashboard(LoginRequiredMixin, TemplateView):
    """
    Team dashboard (home)
    """

    template_name = "home/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        """Email validation guard"""
        if not request.user.profile.email_validated:
            return HttpResponseRedirect(reverse("user:user_email_validation_pending"))

        """Active team guard"""
        teams = request.user.teams.all()
        if not len(teams):
            messages.error(request, "You have no current team memberships.")
        if not len(teams.filter(verified=True)):
            messages.info(
                request,
                "Your team is pending approval by our team. Please check back soon.",
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        user_data = camelize(UserSerializer(user).data)
        user_teams = user.teams.all()
        team_data = camelize(TeamSerializer(user_teams, many=True).data)
        region_data = camelize(RegionSerializer(Region.objects.all(), many=True).data)

        return {"regions": region_data, "teams": team_data, "user": user_data}
