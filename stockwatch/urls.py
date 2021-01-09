"""stockwatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import json

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView

from stock import views as stock_views
from .views import page_not_found


class CustomTokenView(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token)
                app_authorized.send(
                    sender=self, request=request,
                    token=token)
                body['investor'] = {
                    'id': token.user.id,
                    'username': token.user.username
                }
                body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response


urlpatterns = [
    path('api/v1/stockwatch_admin/', admin.site.urls),
    path('api/v1/stockwatch_admin/o/token/', CustomTokenView.as_view(), name='token'),
    path('api/v1/stockwatch_admin/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/v1/investor/', include('investor.urls')),
    path('api/v1/stockNames/', stock_views.stock_names, name='stock_names'),

]

handler404 = page_not_found
handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'
