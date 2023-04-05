import os
import unittest

from speechkit import Session
from speechkit.utils import list_of_service_accounts


class ListOfServiceAccountsTestCase(unittest.TestCase):
    def test_request(self):
        api_key = os.environ.get('YANDEX_OAUTH')
        folder_id = os.environ.get('CATALOG')

        session = Session.from_yandex_passport_oauth_token(api_key, folder_id)

        data = list_of_service_accounts(session)
        self.assertIsInstance(data, list)

    def invalid_session_from_api_key(self):
        session = Session.from_api_key('api_key', 'sdsas')
        with self.assertRaises(ValueError):
            list_of_service_accounts(session)

    def invalid_session_no_folder_id(self):
        api_key = os.environ.get('YANDEX_OAUTH')
        session = Session.from_api_key(api_key)
        with self.assertRaises(ValueError):
            list_of_service_accounts(session)
