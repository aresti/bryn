from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods


from .models import ServerLease
from .serializers import ServerLeaseSerializer


@require_http_methods(["GET", "POST"])
def server_lease_renewal_view(request, server_id, renewal_count):
    """
    GET: Renew server lease and redirect to login (with message)
    POST: Renew server lease and return json serialized representation
    """

    did_renew = False

    # Renew lease
    lease = get_object_or_404(ServerLease, server_id=server_id)
    if lease.renewal_count == renewal_count:
        lease.renew_lease(user=request.user)
        did_renew = True

    # GET: Redirect with message
    if request.method == "GET":
        if did_renew:
            messages.success(
                request,
                f"The lease for server {lease.server_name} has been renewed for {settings.SERVER_LEASE_DEFAULT_DAYS} "
                "days.",
            )
        else:
            messages.warning(
                request,
                "This server lease has already been renewed.",
            )
        return HttpResponseRedirect(reverse("home:home"))

    # POST: Return JSON serialized representation
    serialized = ServerLeaseSerializer(lease)
    return JsonResponse(serialized.data)
