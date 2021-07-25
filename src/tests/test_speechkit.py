import unittest

import speechkit


class InvalidDataErrorTestCase(unittest.TestCase):
    def test_raise(self):
        with self.assertRaises(speechkit.InvalidDataError):
            raise speechkit.InvalidDataError()


class RequestErrorTestCase(unittest.TestCase):
    def test_raise_data_1(self):
        with self.assertRaises(speechkit.RequestError) as cm:
            raise speechkit.RequestError({'code': 3, 'message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, 3)
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')

    def test_raise_data_2(self):
        with self.assertRaises(speechkit.RequestError) as cm:
            raise speechkit.RequestError({'error_code': 3, 'error_message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, 3)
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')


class RecognizeShortAudioTestCase(unittest.TestCase):
    def test_assert_wrong_key(self):
        with self.assertRaises(speechkit.RequestError):
            speechkit.RecognizeShortAudio('lol')

    def test_init(self):
        pass


class ObjectStorageTestCase(unittest.TestCase):
    pass


class RecognizeLongAudio(unittest.TestCase):
    pass


class SynthesizeAudio(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
