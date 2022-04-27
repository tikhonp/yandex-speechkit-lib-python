import functools
import time

import jwt
import requests

from speechkit.exceptions import RequestError


def generate_jwt(service_account_id, key_id, private_key, exp_time=360):
    """
    Generating JWT token for authorisation

    :param string service_account_id: The ID of the service account whose key the JWT is signed with.
    :param string key_id: The ID of the Key resource belonging to the service account.
    :param bytes private_key: Private key given from Yandex Cloud console in bytes
    :param integer exp_time: Optional. The token expiration time delta in seconds. The expiration
        time must not exceed the issue time by more than one hour, meaning exp_time ≤ 3600. Default 360
    :return: JWT token
    :rtype: string
    """
    if not isinstance(service_account_id, str) or not isinstance(key_id, str):
        raise ValueError("service_account_id, key_id, must be strings.")
    if 0 in (len(service_account_id), len(key_id)):
        raise ValueError("service_account_id, key_id, can't be empty.")
    if not isinstance(private_key, bytes):
        raise ValueError("private_key must be bytes string, but got {}".format(type(private_key)))
    if not isinstance(exp_time, int):
        raise ValueError("exp_time must be int, but got {}".format(type(exp_time)))
    if exp_time > 3600:
        raise ValueError("exp_time ≤ 3600, but got {}".format(exp_time))

    now = int(time.time())
    payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + exp_time
    }
    return jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id}
    )


def get_iam_token(yandex_passport_oauth_token=None, jwt_token=None):
    """
    Creates an IAM token for the specified identity.
    `Getting IAM for Yandex account <https://cloud.yandex.com/en/docs/iam/operations/iam-token/create>`_

    :param string yandex_passport_oauth_token: OAuth token from Yandex OAuth
    :param string jwt_token: Json Web Token, can be generated by :py:meth:`speechkit.generate_jwt`
    :return: IAM token
    :rtype: string
    """
    if not type(yandex_passport_oauth_token) in (str, type(None)):
        raise TypeError("__init__() yandex_passport_oauth_token: got {} but expected \
                        type is str or None".format(type(yandex_passport_oauth_token).__name__))

    if not type(jwt_token) in (str, type(None)):
        raise TypeError("__init__() jwt_token: got {} but expected \
                        type is str or None".format(type(jwt_token).__name__))

    if (not yandex_passport_oauth_token and not jwt_token) or (yandex_passport_oauth_token and jwt_token):
        raise ValueError("Includes only one of the fields `yandex_passport_oauth_token`, `jwt_token`")

    if yandex_passport_oauth_token:
        data = {'yandexPassportOauthToken': str(yandex_passport_oauth_token)}
    else:
        data = {'jwt': str(jwt_token)}

    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    answer = requests.post(url, json=data)

    if answer.ok:
        return answer.json().get('iamToken')
    else:
        raise RequestError(answer.json())


def get_api_key(yandex_passport_oauth_token=None, service_account_id=None,
                description='Default Api-Key created by `speechkit` python SDK'):
    """
    Creates an API key for the specified service account.

    :param string yandex_passport_oauth_token: OAuth token from Yandex OAuth
    :param string service_account_id: The ID of the service account whose key the Api-Key is signed with.
    :param string description: Description for api-key. Optional.
    :return: Api-Key
    :rtype: string
    """
    if not yandex_passport_oauth_token or not service_account_id:
        raise ValueError("`yandex_passport_oauth_token` and `service_account_id` required.")

    url = 'https://iam.api.cloud.yandex.net/iam/v1/apiKeys'
    headers = {
        'Authorization': 'Bearer {}'.format(get_iam_token(yandex_passport_oauth_token=yandex_passport_oauth_token))
    }
    data = {'serviceAccountId': service_account_id, 'description': description}

    answer = requests.post(url, headers=headers, json=data)
    if answer.ok:
        return answer.json().get('secret')
    else:
        raise RequestError(answer.json())


class Session:
    """Class provides yandex API authentication."""

    IAM_TOKEN = 'iam_token'
    """Iam_token if iam auth, value: 'iam_token'"""

    API_KEY = 'api_key'
    """Api key if api-key auth, value: 'api_key'"""

    def __init__(self, auth_type, credential, folder_id):
        """
        Stores credentials for given auth method

        :param string auth_type: Type of auth may be :py:meth:`Session.IAM_TOKEN` or :py:meth:`Session.API_KEY`
        :param string | None folder_id: Id of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.
        :param string credential: Auth key iam or api key
        """
        if auth_type not in (self.IAM_TOKEN, self.API_KEY):
            raise ValueError(
                "auth_type must be `Session.IAM_TOKEN` or `Session.API_KEY`, but given {}".format(auth_type)
            )

        self._auth_method = auth_type

        if not isinstance(credential, str):
            raise ValueError("_credential must be string, but got {}".format(type(credential)))

        self._credential = credential
        self.folder_id = folder_id

    @classmethod
    def from_api_key(cls, api_key, folder_id=None):
        """
        Creates session from api key

        :param string api_key: Yandex Cloud Api-Key
        :param string | None folder_id: Id of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.
        :return: Session instance
        :rtype: Session
        """
        if not isinstance(api_key, str):
            raise ValueError("Api-Key must be string, but got {}".format(type(api_key)))
        if len(api_key) == 0:
            raise ValueError("Api-Key can not be empty.")

        if folder_id:
            if not isinstance(folder_id, str):
                raise ValueError("folder_id must be string, but got {}".format(type(folder_id)))
            if len(folder_id) == 0:
                raise ValueError("folder_id must not be empty.")

        return cls(cls.API_KEY, api_key, folder_id=folder_id)

    @classmethod
    def from_yandex_passport_oauth_token(cls, yandex_passport_oauth_token, folder_id):
        """
        Creates Session from oauth token Yandex account

        :param string yandex_passport_oauth_token: OAuth token from Yandex.OAuth
        :param string folder_id: Id of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.
        :return: Session instance
        :rtype: Session
        """
        if not isinstance(yandex_passport_oauth_token, str):
            raise ValueError(
                "yandex_passport_oauth_token must be string, but got {}".format(type(yandex_passport_oauth_token))
            )
        if len(yandex_passport_oauth_token) == 0:
            raise ValueError("yandex_passport_oauth_token can not be empty.")

        if not isinstance(folder_id, str):
            raise ValueError("folder_id must be string, but got {}".format(type(folder_id)))
        if len(folder_id) == 0:
            raise ValueError("folder_id must not be empty.")

        iam_token = get_iam_token(yandex_passport_oauth_token=yandex_passport_oauth_token)

        return cls(cls.IAM_TOKEN, iam_token, folder_id=folder_id)

    @classmethod
    def from_jwt(cls, jwt_token, folder_id=None):
        """
        Creates Session from JWT token

        :param string jwt_token: JWT
        :param string | None folder_id: Id of the folder that you have access to. Don't specify this field if
            you make a request on behalf of a service account.
        :return: Session instance
        :rtype: Session
        """
        if not isinstance(jwt_token, str):
            raise ValueError("jwt_token must be string, but got {}".format(type(jwt_token)))
        if len(jwt_token) == 0:
            raise ValueError("jwt_token can not be empty.")

        if folder_id:
            if not isinstance(folder_id, str):
                raise ValueError("folder_id must be string, but got {}".format(type(folder_id)))
            if len(folder_id) == 0:
                raise ValueError("folder_id must not be empty.")

        iam_token = get_iam_token(jwt_token=jwt_token)

        return cls(cls.IAM_TOKEN, iam_token, folder_id=folder_id)

    @property
    def header(self):
        """
        Authentication header.

        :return: Dict in format `{'Authorization': 'Bearer or Api-Key {iam or api_key}'}`
        :rtype: dict
        """
        if self._auth_method == self.IAM_TOKEN:
            return {'Authorization': 'Bearer {iam}'.format(iam=self._credential)}
        if self._auth_method == self.API_KEY:
            return {'Authorization': 'Api-Key {api_key}'.format(api_key=self._credential)}

    @property
    def streaming_recognition_header(self):
        """
        Authentication header for streaming recognition

        :return: Tuple in format `('authorization', 'Bearer or Api-Key {iam or api_key}')`
        :rtype: tuple
        """

        if self._auth_method == self.IAM_TOKEN:
            return tuple(('authorization', 'Bearer {iam}'.format(iam=self._credential),))
        if self._auth_method == self.API_KEY:
            return tuple(('authorization', 'Api-Key {api_key}'.format(api_key=self._credential),))

    @property
    def auth_method(self):
        return self._auth_method
