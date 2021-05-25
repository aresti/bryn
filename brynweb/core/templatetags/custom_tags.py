from urllib.parse import urljoin

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_str
from django.utils.functional import keep_lazy
from django.utils.safestring import SafeText, mark_safe

register = template.Library()

_slack_escapes = {
    ord("&"): "&amp;",
    ord("<"): "&lt;",
    ord(">"): "&gt;",
}


@register.filter
@stringfilter
def absolute_url(value):
    scheme = getattr(settings, "SITE_SCHEME", "http")
    domain = getattr(settings, "SITE_DOMAIN", "localhost:8000")
    base_url = f"{scheme}://{domain}"
    return urljoin(base_url, value)


#  Taken from django_slack
@keep_lazy(str, SafeText)
@register.filter(is_safe=True)
@stringfilter
def escapeslack(value):
    """
    Returns the given text with ampersands and angle brackets encoded for use in
    the Slack API, per the Slack API documentation:
    <https://api.slack.com/docs/formatting#how_to_escape_characters>
    This is based on django.template.defaultfilters.escapejs.
    """
    return mark_safe(force_str(value).translate(_slack_escapes))
