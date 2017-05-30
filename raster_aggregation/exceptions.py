from __future__ import unicode_literals

from rest_framework.exceptions import APIException


class MissingQueryParameter(APIException):
    status_code = 400
    default_detail = 'Missing Query Parameter.'
