import json

from rest_framework.test import APITestCase, APIRequestFactory
from .views import DomainApiView, LinkApiView


class TestLinkView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LinkApiView.as_view()
        self.uri = '/visited_links/'

    def test_list(self):
        data_ok = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
        data_fail = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "notlink",
                "https://i_am_link.com",
                "i_am_link_too.com"
            ]
        }
        data_fail_2 = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "not.link.",
                "not.link....",
                "https://i_am_link.com",
                "i_am_link_too.com"
            ]
        }
        request_ok = self.factory.post(self.uri, data=json.dumps(data_ok), content_type='application/json')
        request_fail = self.factory.post(self.uri, data=json.dumps(data_fail), content_type='application/json')
        request_fail_2 = self.factory.post(self.uri, data=json.dumps(data_fail_2), content_type='application/json')
        response_ok = self.view(request_ok)
        response_fail = self.view(request_fail)
        response_fail_2 = self.view(request_fail_2)
        self.assertEqual(response_ok.status_code, 201,
                         'Expected Response Code 201, received {} with resp {} instead.'
                         .format(response_ok.status_code, response_ok.data))
        self.assertEqual(response_fail.status_code, 400,
                         'Expected Response Code 400, received {} with resp {} instead.'
                         .format(response_fail.status_code, response_fail.data))
        self.assertEqual(response_fail_2.status_code, 400,
                         'Expected Response Code 400, received {} with resp {} instead.'
                         .format(response_fail_2.status_code, response_fail_2.data))


class TestDomainView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DomainApiView.as_view()
        self.uri = '/visited_domains/'

    def test_list(self):
        request_ok = self.factory.get(self.uri, data={'from': '2020-05-26', 'to': '2020-05-28'})
        request_fail = self.factory.get(self.uri, data={'from': '2020.05.26', 'to': '20200528'})
        request_fail_2 = self.factory.get(self.uri, data={'from': '2020-05-23', 'to': '2020-05-25'})
        response_ok = self.view(request_ok)
        response_fail = self.view(request_fail)
        response_fail_2 = self.view(request_fail_2)
        self.assertEqual(response_ok.status_code, 200,
                         'Expected Response Code 200, received {} with resp {} instead.'
                         .format(response_ok.status_code, response_ok.data))
        self.assertEqual(response_fail.status_code, 400,
                         'Expected Response Code 400, received {} with resp {} instead.'
                         .format(response_fail.status_code, response_fail.data))
        self.assertEqual(response_fail_2.status_code, 204,
                         'Expected Response Code 204, received {} with resp {} instead.'
                         .format(response_fail_2.status_code, response_fail_2.data))
