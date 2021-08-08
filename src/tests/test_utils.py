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
