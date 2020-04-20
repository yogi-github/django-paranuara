from django.test import TestCase

from helpers.app_response import AppResponse


class AppResponseTest(TestCase):

    def test_response_for_code_200(self):

        response = AppResponse(data={'test': 123}, message='test', status=200)

        value = response.data
        self.assertDictEqual(value['data'], {'test': 123})
        self.assertEqual(value['message'], 'test')
        self.assertEqual(value['status_message'], 'ok')

    def test_response_for_code_400(self):

        response = AppResponse(data={'test': 123}, message='test', status=400)

        value = response.data
        self.assertDictEqual(value['data'], {'test': 123})
        self.assertEqual(value['message'], 'test')
        self.assertEqual(value['status_message'], 'client_error')

    def test_response_for_invalid_status(self):

        self.assertRaises(ValueError, AppResponse, data={'test': 123}, message='test', status=999)

    def test_response_for_none_status(self):

        response = AppResponse(data={'test': 123}, message='test')

        value = response.data
        self.assertDictEqual(value['data'], {'test': 123})
        self.assertEqual(value['message'], 'test')
        self.assertEqual(value['status_message'], '')
