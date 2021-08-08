"""Utilities functions, tht allow to use different api methods."""

import requests

from speechkit.exceptions import RequestError


def list_of_service_accounts(session, **kwargs):
    """
    Retrieves the list of ServiceAccount resources in the specified folder.

    :param speechkit._auth.Session session: Session instance for auth
    :param dict kwargs: Additional parameters
    :return: List of dict with data of services accounts
    :rtype: list[dict]
    """
    if session.auth_method == session.API_KEY:
        raise ValueError("Api-Key authorisation method is invalid.")
    if session.folder_id is None:
        raise ValueError("You must specify folder is in session.")

    headers = session.header
    url = 'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts'
    data = {'folderId': session.folder_id, **kwargs}
    answer = requests.get(url, headers=headers, json=data)

    if answer.ok:
        return answer.json().get('serviceAccounts', [])
    else:
        raise RequestError(answer.json())
