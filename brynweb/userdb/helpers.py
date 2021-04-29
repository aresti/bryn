def get_teams_for_user(user, team=None, admin=None):
    """
    Return a queryset for all verified teams that an authenticated user is a member of.
    If team is specified, returns a queryset with only that team, if the user is a member.
    If team & admin are specified, returns a query set with only that team, if the user is an admin.
    """
    user_teams = user.teams.filter(verified=True)
    if team:
        if admin:
            return user_teams.filter(pk=team, memberships__is_admin=True)
        return user_teams.filter(pk=team)
    else:
        return user_teams
