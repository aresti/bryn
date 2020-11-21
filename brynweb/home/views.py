from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from userdb.serializers import TeamSerializer, UserSerializer


class TeamDashboard(LoginRequiredMixin, TemplateView):
    """
    Team dashboard (home)
    """

    template_name = "home/dashboard.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        user_data = UserSerializer(user).data
        user_teams = user.teams.all()
        team_data = TeamSerializer(user_teams, many=True).data
        return {"teams": team_data, "user": user_data}
