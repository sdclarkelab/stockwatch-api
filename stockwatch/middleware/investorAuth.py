import re

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

from utils.custom_json_resp import CustomJsonResponse


class InvestorAuthorizationMiddleware(MiddlewareMixin):
    """
    Ensures that the investor can view only their data.
    :param MiddlewareMixin:
    :return:
    """
    def process_request(self, request):

        # Intercept investor endpoint to
        if ('api/v1/investor' in request.path) and (not request.method == 'POST') and request.user:

            # Extract investor id from request path
            if re.search('/investor/(\d+)', request.path):
                investor_id = re.search('/investor/(\d+)', request.path).group(1)

                if request.user.id != int(investor_id):
                    return JsonResponse(CustomJsonResponse.return_user_unauth(), status=status.HTTP_403_FORBIDDEN)
