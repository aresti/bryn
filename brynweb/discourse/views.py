# from https://meta.discourse.org/t/sso-example-for-django/14258

import base64
import hmac
import hashlib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings

from urllib.parse import parse_qs, unquote, urlencode


@login_required
def sso(request):
    payload = request.GET.get("sso")
    signature = request.GET.get("sig")

    if None in [payload, signature]:
        return HttpResponseBadRequest(
            "No SSO payload or signature. Please contact support if this problem persists."
        )

    # Validate the payload

    try:
        payload = unquote(payload).encode("ascii")
        decoded = base64.b64decode(payload).decode("ascii")
        # assert "nonce" in decoded
        # assert len(payload) > 0
    except AssertionError:
        return HttpResponseBadRequest(
            "Invalid payload. Please contact support if this problem persists."
        )

    key = settings.DISCOURSE_SSO_SECRET.encode("ascii")
    h = hmac.new(key, payload, digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        return HttpResponseBadRequest(
            "Invalid payload. Please contact support if this problem persists."
        )

    # Build the return payload

    qs = parse_qs(decoded)
    params = {
        "nonce": qs["nonce"][0],
        "email": request.user.email,
        "external_id": request.user.id,
        "username": request.user.username,
    }

    return_payload = base64.b64encode(urlencode(params).encode("ascii"))
    h = hmac.new(key, return_payload, digestmod=hashlib.sha256)
    query_string = urlencode({"sso": return_payload, "sig": h.hexdigest()})

    # Redirect back to Discourse

    url = "%s/session/sso_login" % settings.DISCOURSE_BASE_URL
    return HttpResponseRedirect("%s?%s" % (url, query_string))
