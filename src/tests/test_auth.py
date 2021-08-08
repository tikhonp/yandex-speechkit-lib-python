import os
import unittest
from unittest import TestCase

from speechkit.auth import generate_jwt, get_iam_token, get_api_key
from speechkit import Session


class GenerateJwtTestCase(unittest.TestCase):
    def test_generating(self):
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
        key_id = os.environ.get('YANDEX_KEY_ID')
        private_key = os.environ.get('YANDEX_PRIVATE_KEY').replace('\\n', '\n').encode()
        jwt = generate_jwt(service_account_id, key_id, private_key)
        self.assertIsInstance(jwt, str)


class GetIamTokenTestCase(unittest.TestCase):
    def test_assert_empty_data(self):
        with self.assertRaises(ValueError):
            get_iam_token()

    def test_assert_invalid_data(self):
        with self.assertRaises(ValueError):
            get_iam_token(yandex_passport_oauth_token='', jwt_token='')

    def test_request_yandex_oauth(self):
        oauth_token = os.environ.get('YANDEX_OAUTH')

        data = get_iam_token(yandex_passport_oauth_token=oauth_token)
        self.assertIsInstance(data, str)

    def test_request_jwt(self):
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
        key_id = os.environ.get('YANDEX_KEY_ID')
        private_key = os.environ.get('YANDEX_PRIVATE_KEY').replace('\\n', '\n').encode()
        jwt = generate_jwt(service_account_id, key_id, private_key)

        data = get_iam_token(jwt_token=jwt)
        self.assertIsInstance(data, str)


class GetApiKeyTestCase(unittest.TestCase):
    def test_request(self):
        yandex_passport_oauth_token = os.environ.get('YANDEX_OAUTH')
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')

        data = get_api_key(yandex_passport_oauth_token, service_account_id)
        self.assertIsInstance(data, str)


class SessionTestCase(TestCase):
    def test_from_api_key(self):
        api_key = os.environ.get('SERVICE_API_KEY')
        folder_id = os.environ.get('CATALOG')

        session = Session.from_api_key(api_key, folder_id)
        self.assertIsInstance(session.header, dict)
        self.assertEqual(session.folder_id, folder_id)

    def test_from_yandex_passport_oauth_token(self):
        oauth_token = os.environ.get('YANDEX_OAUTH')
        folder_id = os.environ.get('CATALOG')

        session = Session.from_yandex_passport_oauth_token(oauth_token, folder_id)
        self.assertIsInstance(session.header, dict)

    def test_from_jwt(self):
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
        key_id = os.environ.get('YANDEX_KEY_ID')
        private_key = os.environ.get('YANDEX_PRIVATE_KEY').replace('\\n', '\n').encode()
        jwt = generate_jwt(service_account_id, key_id, private_key)

        session = Session.from_jwt(jwt)
        self.assertIsInstance(session.header, dict)

    def test_header_api_key(self):
        session = Session(Session.API_KEY, 'hello', None)
        self.assertEqual(session.header, {'Authorization': 'Api-Key hello'})

    def test_header_iam_token(self):
        session = Session(Session.IAM_TOKEN, 'hello', None)
        self.assertEqual(session.header, {'Authorization': 'Bearer hello'})


if __name__ == '__main__':
    unittest.main()
