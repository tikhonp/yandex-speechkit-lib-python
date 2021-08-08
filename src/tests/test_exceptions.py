import unittest

from speechkit.exceptions import RequestError


class RequestErrorTestCase(unittest.TestCase):
    def test_raise_data_1(self):
        with self.assertRaises(RequestError) as cm:
            raise RequestError({'code': 3, 'message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, '3')
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')

    def test_raise_data_2(self):
        with self.assertRaises(RequestError) as cm:
            raise RequestError({'error_code': 3, 'error_message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, '3')
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')
