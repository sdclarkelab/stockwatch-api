import json

from django.http import HttpResponseNotFound


def page_not_found(request, exception):
    response_data = {'error': 'Not found.'}
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")
