import re
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Link
from core.utils import transform_data


def validate_data(data: dict):
    try:
        links = data['links']
    except KeyError:
        return Response(data={'status': 'data must contains `links` list'}, status=status.HTTP_400_BAD_REQUEST)
    for link in links:
        if link is None:
            return Response(data={'status': 'link can not be `None`'}, status=status.HTTP_400_BAD_REQUEST)
        if type(link) is not str:
            return Response(data={'status': 'expected `str` link, not `{}`'.format(type(link))},
                            status=status.HTTP_400_BAD_REQUEST)
        if not link.startswith(('http://', 'https://')):
            if re.fullmatch(r'(\w+.?)*', link) is None or link.find('.') < 0:
                return Response(data={'status': 'data must contains only links'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data=links, status=200)


def validate_filter(filter_params: dict):
    validate_res = filter_params
    try:
        validate_res['from'] = datetime.strptime(validate_res['from'][0], '%Y-%m-%d')
        validate_res['to'] = datetime.strptime(validate_res['to'][0], '%Y-%m-%d')
    except (KeyError, ValueError) as e:
        return Response(data={'status': 'Missing requirement filter argument or invalid date format. More in extra',
                              'extra': '`{}`'.format(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(validate_res['from'].date())) or \
            not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(validate_res['from'].date())):
        return Response(data={'status': 'filter parameters must in format like `YYYY-mm-dd`'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(data=validate_res, status=200)


class DomainApiView(APIView):
    def get(self, request):
        validator = validate_filter(dict(self.request.GET))
        if validator.status_code is not 200:
            return validator
        qs = Link.filter_qs(validator.data)
        if len(qs) == 0:
            return Response(data={'status': 'Does not match query with yours parameters'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response(data={'domains': list(set([link.link for link in qs])), 'status': 'ok'},
                        status=status.HTTP_200_OK)


class LinkApiView(APIView):
    def post(self, request):
        validate_resp = validate_data(self.request.data)
        if validate_resp.status_code is not 200:
            return validate_resp
        links = transform_data(validate_resp.data)
        for link in links:
            try:
                model = Link(link=link)
                model.save()
            except BaseException as e:
                return Response(data={'status': '{}'.format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'status': 'ok'}, status=status.HTTP_201_CREATED)
