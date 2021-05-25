import traceback

from django.conf import settings

from .utils import slack_post_templated_message


class SlackErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if settings.DEBUG:
            return

        context = {
            "url": request.build_absolute_uri(),
            "error": repr(exception),
            "traceback": traceback.format_exc(),
            "user": request.user,
        }
        slack_post_templated_message("slack/error_traceback.txt", context=context)
