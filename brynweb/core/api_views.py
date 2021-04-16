from django.conf import settings
from django.contrib.messages import get_messages
from django.core import management

from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import MessageSerializer


class MessagesListView(APIView):
    """
    API List endpoint for Django messages framework
    """

    def get(self, request):
        serialized_messages = MessageSerializer(
            [message for message in get_messages(request)], many=True
        )
        return Response(serialized_messages.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_db_for_tests(request):
    """
    API endpoint to flush and reseed database for testing. DEBUG only.
    """
    if settings.DEBUG:
        management.call_command("flush", interactive=False)
        management.call_command(
            "loaddata", "frontend/cypress/fixtures/default_seed.json"
        )
        return Response("Database reset")
    raise PermissionDenied("Database cannot be reset in production")
