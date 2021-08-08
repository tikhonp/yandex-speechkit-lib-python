"""
Utilities for Yandex Cloud authorisation
`IAM token <https://cloud.yandex.com/en/docs/iam/concepts/authorization/iam-token>`_
`Api-Key <https://cloud.yandex.com/en/docs/iam/concepts/authorization/api-key>`_
"""

from speechkit._auth import generate_jwt, get_iam_token, get_api_key

__all__ = ['generate_jwt', 'get_iam_token', 'get_api_key']
