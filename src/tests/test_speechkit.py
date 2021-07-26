import os
import pathlib
import time
import unittest
import warnings

import speechkit

test_data = b'RIFFl@\x08\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\xbb\x00\x00\x00w\x01\x00\x02\x00\x10\x00LIST@\x00\x00\x00INFOINAM\x1d\x00\x00\x00\xd1\x83\xd0\xbb\xd0\xb8\xd1\x86\xd0\xb0 8 \xd0\x9c\xd0\xb0\xd1\x80\xd1\x82\xd0\xb0, 6 9\x00\x00ISFT\x0e\x00\x00\x00Lavf58.76.100\x00data\x00@\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x00\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x02\x00\x02\x00\x01\x00\x01\x00\x01\x00\x01\x00\x02\x00\x02\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x02\x00\x02\x00\x02\x00\x02\x00\x02\x00\x01\x00\x00\x00\x00\x00\x01\x00\x02\x00\x02\x00\x03\x00\x02\x00\x02\x00\x01\x00\xff\xff\xff\xff\x00\x00\xff\xff\xfe\xff\xff\xff\x02\x00\x03\x00\x00\x00\xfd\xff\xfe\xff\x02\x00\x03\x00\x01\x00\xfe\xff\x01\x00\x04\x00\x03\x00\xfe\xff\xfb\xff\xfd\xff\x01\x00\x02\x00\x00\x00\xfc\xff\xfb\xff\xfc\xff\xff\xff\x02\x00\xff\xff\xf2\xff\xe0\xff\xd3\xff\xcf\xff\xd0\xff\xcc\xff\xc4\xff\xbd\xff\xb5\xff\xa5\xff\x8d\xfft\xffd\xff\\\xffX\xffV\xffV\xffV\xffN\xff?\xff1\xff/\xff8\xffA\xffG\xffJ\xffN\xffO\xffL\xffF\xffF\xffH\xffG\xff<\xff.\xff(\xff(\xff&\xff\x1e\xff\x16\xff\x18\xff#\xff0\xff8\xff<\xffA\xffF\xffH\xffH\xffL\xffV\xffb\xffm\xffs\xffv\xffy\xff}\xff\x85\xff\x8f\xff\x9a\xff\xa1\xff\xa8\xff\xaf\xff\xb4\xff\xb6\xff\xb7\xff\xbd\xff\xcc\xff\xdd\xff\xec\xff\xf9\xff\x08\x00\x18\x00\'\x003\x00?\x00J\x00Q\x00T\x00T\x00T\x00S\x00S\x00Z\x00n\x00\x87\x00\x99\x00\xa2\x00\xab\x00\xbb\x00\xcb\x00\xd4\x00\xd3\x00\xce\x00\xc9\x00\xc1\x00\xb4\x00\xa6\x00\x99\x00\x8b\x00~\x00w\x00z\x00\x80\x00\x80\x00w\x00n\x00k\x00o\x00q\x00n\x00j\x00k\x00p\x00q\x00h\x00Y\x00K\x00G\x00G\x00I\x00M\x00V\x00`\x00b\x00]\x00Y\x00X\x00T\x00D\x001\x00(\x00\'\x00 \x00\x0f\x00\xff\xff\xff\xff\t\x00\x0e\x00\x08\x00\xff\xff\xff\xff\x03\x00\x07\x00\t\x00\t\x00\x07\x00\x04\x00\x08\x00\x18\x00,\x005\x007\x00>\x00P\x00_\x00`\x00Y\x00Y\x00e\x00s\x00z\x00\x7f\x00\x85\x00\x8c\x00\x8f\x00\x8e\x00\x8d\x00\x8a\x00\x80\x00r\x00h\x00h\x00n\x00r\x00n\x00j\x00l\x00s\x00w\x00u\x00m\x00f\x00_\x00U\x00F\x008\x001\x00/\x00+\x00"\x00\x1a\x00\x16\x00\x0e\x00\xf9\xff\xda\xff\xbd\xff\xa7\xff\x90\xffs\xffX\xffH\xffA\xff6\xff#\xff\x12\xff\x0c\xff\x0b\xff\x05\xff\xf8\xfe\xed\xfe\xec\xfe\xed\xfe\xea\xfe\xe2\xfe\xde\xfe\xe0\xfe\xe4\xfe\xe5\xfe\xe4\xfe\xe3\xfe\xe1\xfe\xde\xfe\xdb\xfe\xdc\xfe\xe1\xfe\xe3\xfe\xe0\xfe\xde\xfe\xe1\xfe\xe7\xfe\xec\xfe\xf0\xfe\xfc\xfe\x10\xff!\xff\'\xff\'\xff-\xff<\xffJ\xffQ\xffV\xff]\xffe\xfff\xffa\xff\\\xff\\\xff`\xffh\xffs\xff\x81\xff\x8d\xff\x9a\xff\xa9\xff\xbc\xff\xcf\xff\xdf\xff\xf1\xff\x06\x00\x18\x00\x1f\x00!\x00,\x00E\x00^\x00m\x00v\x00\x82\x00\x91\x00\x9b\x00\x9f\x00\xa7\x00\xb8\x00\xcb\x00\xd9\x00\xe2\x00\xee\x00\xfb\x00\x04\x01\x05\x01\x02\x01\x01\x01\x01\x01\xff\x00\xfa\x00\xf4\x00\xec\x00\xe5\x00\xe3\x00\xe6\x00\xed\x00\xf5\x00\x01\x01\x0e\x01\x14\x01\x14\x01\x11\x01\x14\x01\x19\x01\x19\x01\x11\x01\x06\x01\xfc\x00\xf4\x00\xee\x00\xeb\x00\xe9\x00\xe5\x00\xde\x00\xd8\x00\xd5\x00\xce\x00\xbe\x00\xae\x00\xa8\x00\xaa\x00\xa3\x00\x91\x00\x83\x00\x86\x00\x91\x00\x90\x00\x82\x00v\x00r\x00l\x00[\x00H\x00A\x00F\x00G\x00=\x000\x00)\x00\'\x00$\x00\x1b\x00\x11\x00\n\x00\x07\x00\x05\x00\x01\x00\xf8\xff\xe9\xff\xd8\xff\xcc\xff\xc3\xff\xb6\xff\xa2\xff\x91\xff\x8a\xff\x90\xff\x9b\xff\xa4\xff\xad\xff\xba\xff\xcb\xff\xda\xff\xe5\xff\xef\xff\xf9\xff\xff\xff\xfe\xff\xfa\xff\xfa\xff\x02\x00\x08\x00\n\x00\x0e\x00\x1e\x004\x00D\x00K\x00U\x00k\x00\x84\x00\x92\x00\x99\x00\xa9\x00\xc3\x00\xd9\x00\xe3\x00\xec\x00\x02\x01\x1c\x01.\x017\x01D\x01X\x01d\x01^\x01T\x01U\x01^\x01^\x01P\x01C\x01C\x01N\x01W\x01\\\x01b\x01l\x01w\x01\x7f\x01\x84\x01\x83\x01|\x01u\x01q\x01o\x01g\x01W\x01F\x01<\x017\x012\x01)\x01"\x01\x1d\x01\x1b\x01\x16\x01\n\x01\xf5\x00\xd7\x00\xb6\x00\x9c\x00\x87\x00o\x00S\x007\x00$\x00\x1c\x00\x14\x00\x07\x00\xf4\xff\xe1\xff\xd0\xff\xc1\xff\xb1\xff\x9f\xff\x8e\xff\x82\xff|\xffz\xfft\xffj\xff`\xffZ\xffT\xffL\xffC\xff:\xff4\xff-\xff%\xff\x1b\xff\x11\xff\x08\xff\xff\xfe\xfa\xfe\xf8\xfe\xf7\xfe\xf3\xfe\xec\xfe\xe4\xfe\xdf\xfe\xe0\xfe\xe5\xfe\xed\xfe\xf4\xfe\xfd\xfe\r\xff\x1f\xff,\xff.\xff,\xff3\xffE\xffY\xfff\xffq\xff\x80\xff\x98\xff\xb8\xff\xd9\xff\xf5\xff\x06\x00\x10\x00\x1d\x00.\x00<\x00<\x005\x004\x00:\x00:\x00&\x00\n\x00\xf8\xff\xf5\xff\xf6\xff\xf2\xff\xef\xff\xf3\xff\xfa\xff\xfc\xff\xf9\xff\xfb\xff\x00\x00\x03\x00\x01\x00\xff\xff\x04\x00\x0c\x00\x10\x00\x0e\x00\n\x00\x0b\x00\r\x00\x0f\x00\x0e\x00\x0c\x00\x0c\x00\x0c\x00\x0e\x00\r\x00\x0b\x00\t\x00\x0c\x00\x10\x00\x0f\x00\t\x00\x02\x00\x02\x00\x07\x00\n\x00\n\x00\t\x00\t\x00\t\x00\x07\x00\x06\x00\x05\x00\x04\x00\x01\x00\x00\x00\x01\x00\x00\x00\xfe\xff\xfb\xff\xfb\xff\xfc\xff\xfb\xff\xf8\xff\xf5\xff\xf7\xff\xf9\xff\xf7\xff\xf2\xff\xf1\xff\xf4\xff\xf7\xff\xf5\xff\xf2\xff\xf1\xff\xf2\xff\xf3\xff\xf3\xff\xf2\xff\xf2\xff\xf2\xff\xf1\xff\xef\xff\xed\xff\xec\xff\xed\xff\xef\xff\xf0\xff\xf1\xff\xf2\xff\xf3\xff\xf4\xff\xf5\xff\xf3\xff\xf0\xff\xee\xff\xed\xff\xee\xff\xed\xff\xeb\xff\xea\xff\xeb\xff\xec\xff\xeb\xff\xe9\xff\xe8\xff\xea\xff\xec\xff\xec\xff\xea\xff\xe9\xff\xea\xff\xeb\xff\xea\xff\xe9\xff\xe8\xff\xe9\xff\xe9\xff\xea\xff\xea\xff\xe8\xff\xe5\xff\xe2\xff\xe2\xff\xe4\xff\xe4\xff\xe2\xff\xdf\xff\xdf\xff\xe0\xff\xe0\xff\xde\xff\xdd\xff\xdc\xff\xda\xff\xd9\xff\xd9\xff\xdb\xff\xdd\xff\xdc\xff\xd9\xff\xd8\xff\xda\xff\xdb\xff\xdb\xff\xdc\xff\xde\xff\xdd\xff\xda\xff\xd7\xff\xd7\xff\xd8\xff\xd8\xff\xd7\xff\xd7\xff\xd9\xff\xda\xff\xd8\xff\xd6\xff\xd5\xff\xd5\xff\xd5\xff\xd5\xff\xd5\xff\xd5\xff\xd5\xff\xd6\xff\xda\xff\xdd\xff\xde\xff\xde\xff\xde\xff\xe1\xff\xe2\xff\xe1\xff\xe0\xff\xe1\xff\xe3\xff\xe4\xff\xe2\xff\xe1\xff\xe3\xff\xe4\xff\xe4\xff\xe2\xff\xe2\xff\xe4\xff\xe6\xff\xe8\xff\xe9\xff\xe9\xff\xea\xff\xeb\xff\xec\xff\xec\xff\xec\xff\xed\xff\xef\xff\xf0\xff\xef\xff\xed\xff\xed\xff\xee\xff\xef\xff\xee\xff\xec\xff\xeb\xff\xeb\xff\xeb\xff\xea\xff\xea\xff\xe9\xff\xe9\xff\xe8\xff\xe8\xff\xe8\xff\xe7\xff\xe5\xff\xe4\xff\xe4\xff\xe6\xff\xe8\xff\xe8\xff\xe6\xff\xe4\xff\xe4\xff\xe5\xff\xe6\xff\xe6\xff\xe5\xff\xe4\xff\xe3\xff\xe4\xff\xe4\xff\xe3\xff\xe1\xff\xe0\xff\xe0\xff\xe0\xff\xdf\xff\xde\xff\xde\xff\xdd\xff\xdb\xff\xda\xff\xda\xff\xda\xff\xd9\xff\xd8\xff\xd7\xff\xd8\xff\xd8\xff\xd6\xff\xd3\xff\xd2\xff\xd3\xff\xd5\xff\xd7\xff\xda\xff\xdc\xff\xde\xff\xde\xff\xde\xff\xdf\xff\xe0\xff\xe0\xff\xe0\xff\xe1\xff\xe3\xff\xe5\xff\xe4\xff\xe0\xff\xdd\xff\xdd\xff\xe1\xff\xe4\xff\xe4\xff\xe2\xff\xe1\xff\xe2\xff\xe3\xff\xe4\xff\xe5\xff\xe5\xff\xe5\xff\xe4\xff\xe4\xff\xe5\xff\xe6\xff\xe7\xff\xe7\xff\xe6\xff\xe6\xff\xe7\xff\xe7\xff\xe8\xff\xe8\xff\xe8\xff\xe8\xff\xe9\xff\xea\xff\xea\xff\xea\xff\xe9\xff\xe9\xff\xe9\xff\xe9\xff\xe9\xff\xe9\xff\xe8\xff\xe8\xff\xe8\xff\xe8\xff\xe9\xff\xe9\xff\xe8\xff\xe7\xff\xe6\xff\xe7\xff\xe7\xff\xe6\xff\xe5\xff\xe5\xff\xe5\xff\xe6\xff\xe5\xff\xe4\xff\xe4\xff\xe5\xff\xe4\xff\xe4\xff\xe3\xff\xe2\xff\xe2\xff\xe2\xff\xe1\xff\xe0\xff\xe0\xff\xdf\xff\xde\xff\xde\xff\xdd\xff\xdd\xff\xdc\xff\xdc\xff\xdb\xff\xdb\xff\xdb\xff\xda\xff\xda\xff\xda\xff\xda\xff\xd9\xff\xd9\xff\xd9\xff\xd8\xff\xd8\xff\xd9\xff\xd9\xff\xd9\xff\xd9\xff\xd9\xff\xda\xff\xda\xff\xda\xff\xda\xff\xdb\xff\xdb\xff\xdb\xff\xdc\xff\xdc\xff\xdc\xff\xdd\xff\xdd\xff\xde\xff\xde\xff\xdf\xff\xdf\xff\xe0\xff\xe0\xff\xe1\xff\xe1\xff\xe1\xff\xe2\xff\xe2\xff\xe3\xff\xe3\xff\xe3\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe4\xff\xe3\xff\xe3\xff\xe3\xff\xe2\xff\xe2\xff\xe2\xff\xe2\xff\xe1\xff\xe1\xff\xe1\xff\xe1\xff'


class InvalidDataErrorTestCase(unittest.TestCase):
    def test_raise(self):
        with self.assertRaises(speechkit.InvalidDataError):
            raise speechkit.InvalidDataError()


class RequestErrorTestCase(unittest.TestCase):
    def test_raise_data_1(self):
        with self.assertRaises(speechkit.RequestError) as cm:
            raise speechkit.RequestError({'code': 3, 'message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, '3')
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')

    def test_raise_data_2(self):
        with self.assertRaises(speechkit.RequestError) as cm:
            raise speechkit.RequestError({'error_code': 3, 'error_message': 'message'})

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, '3')
        self.assertEqual(the_exception.message, 'message')
        self.assertEqual(str(the_exception), '3 message')


class GetIamTokenTestCase(unittest.TestCase):
    def test_assert_empty_data(self):
        with self.assertRaises(speechkit.InvalidDataError):
            speechkit.get_iam_token()

    def test_assert_invalid_data(self):
        with self.assertRaises(speechkit.InvalidDataError):
            speechkit.get_iam_token(yandex_passport_oauth_token='', jwt='')

    def test_request(self):
        api_key = os.environ.get('API_KEY')

        data = speechkit.get_iam_token(yandex_passport_oauth_token=api_key)
        self.assertIsInstance(data, str)


class GetApiKeyTestCase(unittest.TestCase):
    def test_request(self):
        api_key = os.environ.get('API_KEY')
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')

        data = speechkit.get_api_key(api_key, service_account_id)
        self.assertIsInstance(data, str)


class ListOfServiceAccountsTestCase(unittest.TestCase):
    def test_request(self):
        api_key = os.environ.get('API_KEY')
        folder_id = os.environ.get('CATALOG')
        data = speechkit.list_of_service_accounts(api_key, folder_id)
        self.assertIsInstance(data, list)


class RecognizeShortAudioTestCase(unittest.TestCase):
    def test_assert_wrong_key_and_wrong_token(self):
        with self.assertRaises(speechkit.RequestError):
            speechkit.RecognizeShortAudio('lol')

    def test_init(self):
        api_key = os.environ.get('API_KEY')
        recognize_short_audio = speechkit.RecognizeShortAudio(api_key)
        self.assertIsInstance(recognize_short_audio._headers, dict)

    def test_wrong_catalog(self):
        api_key = os.environ.get('API_KEY')
        recognize_short_audio = speechkit.RecognizeShortAudio(api_key)

        with self.assertRaises(speechkit.RequestError):
            recognize_short_audio.recognize(bytes(), folderId='lol')

    def test_recognize(self):
        api_key = os.environ.get('API_KEY')
        recognize_short_audio = speechkit.RecognizeShortAudio(api_key)

        folder_id = os.environ.get('CATALOG')
        text = recognize_short_audio.recognize(
            test_data, folderId=folder_id,
            format='lpcm', sampleRateHertz='48000'
        )
        self.assertIsInstance(text, str)


class RecognizeLongAudio(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

    def test_init_wrong_description_and_api_key(self):
        with self.assertRaises(speechkit.InvalidDataError):
            speechkit.RecognizeLongAudio(1, 'aid', 'bucket')

        with self.assertRaises(speechkit.InvalidDataError):
            speechkit.RecognizeLongAudio('', '', 'bucket')

        with self.assertRaises(speechkit.InvalidDataError):
            speechkit.RecognizeLongAudio('lol', 'acid', 'bucket', aws_credentials_description='l' * 257)

    def test_assert_wrong_key_and_wrong_token(self):
        with self.assertRaises(speechkit.RequestError):
            speechkit.RecognizeLongAudio('lol', '', 'bucket')

    def test_init(self):
        api_key = os.environ.get('API_KEY')
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
        bucket_name = os.environ.get('BUCKET_NAME')
        recognize_long_audio = speechkit.RecognizeLongAudio(api_key, service_account_id, bucket_name)
        self.assertIsInstance(recognize_long_audio._api_key_headers, dict)

    def test_recognition(self):
        api_key = os.environ.get('API_KEY')
        service_account_id = os.environ.get('SERVICE_ACCOUNT_ID')
        bucket_name = os.environ.get('BUCKET_NAME')

        recognize_long_audio = speechkit.RecognizeLongAudio(api_key, service_account_id, bucket_name)

        self.path = os.path.join(os.path.dirname(__file__), 'test_rec.wav')
        with open(self.path, 'wb') as f:
            f.write(test_data)

        recognize_long_audio.send_for_recognition(
            self.path, audioEncoding='LINEAR16_PCM', sampleRateHertz='48000',
            audioChannelCount=1, rawResults=False
        )

        while True:
            time.sleep(2)
            if recognize_long_audio.get_recognition_results():
                break

        data = recognize_long_audio.get_data()
        self.assertIsInstance(data, (list, type(None)))

        text = recognize_long_audio.get_raw_text()
        self.assertIsInstance(text, str)


class SynthesizeAudio(unittest.TestCase):
    def test_assert_wrong_key_and_wrong_token(self):
        with self.assertRaises(speechkit.RequestError):
            speechkit.SynthesizeAudio('lol')

    def test_init(self):
        api_key = os.environ.get('API_KEY')
        synthesize_audio = speechkit.SynthesizeAudio(api_key)
        self.assertIsInstance(synthesize_audio._headers, dict)

    def test_wrong_catalog(self):
        api_key = os.environ.get('API_KEY')
        synthesize_audio = speechkit.SynthesizeAudio(api_key)

        with self.assertRaises(speechkit.RequestError):
            synthesize_audio.synthesize_stream(text='text', folderId='lol')

    def test_synthesize(self):
        api_key = os.environ.get('API_KEY')
        synthesize_audio = speechkit.SynthesizeAudio(api_key)

        folder_id = os.environ.get('CATALOG')
        self.path = os.path.join(os.path.dirname(__file__), 'test_synth.wav')
        synthesize_audio.synthesize(
            self.path, text='text',
            voice='oksana', format='lpcm', sampleRateHertz='16000',
            folderId=folder_id
        )
        self.assertTrue(pathlib.Path(self.path).resolve().is_file())

    def test_assert_synthesize(self):
        api_key = os.environ.get('API_KEY')
        synthesize_audio = speechkit.SynthesizeAudio(api_key)

        with self.assertRaises(speechkit.InvalidDataError):
            synthesize_audio.synthesize(
                'ok', text='t' * 5001
            )

    def test_synthesize_stream(self):
        api_key = os.environ.get('API_KEY')
        synthesize_audio = speechkit.SynthesizeAudio(api_key)

        folder_id = os.environ.get('CATALOG')
        data = synthesize_audio.synthesize_stream(
            text='text', voice='oksana', format='lpcm',
            sampleRateHertz='16000', folderId=folder_id
        )
        self.assertIsInstance(data, bytes)


if __name__ == '__main__':
    unittest.main()
