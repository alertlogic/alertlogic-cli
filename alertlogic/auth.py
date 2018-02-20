# -*- coding: utf-8 -*-
"""
    alertlogic.auth
    ~~~~~~~~~~~~~~
    alertlogic authentication/authorization
"""

import requests


class AuthenticationException(Exception):
    def __init__(self, message):
        super(AuthenticationException, self).__init__("authentication error: {}".format(message))


class Session():
    """
    Authenticates against alertlogic aims service and stores session information (token and account id),
    additionally objects of this class can be used as auth modules for the requests lib, more info:
    http://docs.python-requests.org/en/master/user/authentication/#new-forms-of-authentication
    """

    def __init__(self, region, username, password):
        """
        :param region: a Region object
        :param username: your alertlogic cloudinsight username
        :param password: your alertlogic cloudinsight password
        """
        self.region = region
        self._authenticate(username, password)

    def _authenticate(self, username, password):
        """
        Authenticates against alertlogic Access and Identity Management Service (AIMS)
        more info:
        https://console.cloudinsight.alertlogic.com/api/aims/#api-AIMS_Authentication_and_Authorization_Resources-Authenticate
        """
        try:
            auth = requests.auth.HTTPBasicAuth(username, password)
            response = requests.post(self.region.get_api_endpoint() + "/aims/v1/authenticate", auth=auth)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise AuthenticationException("invalid http response {}".format(e.message))

        try:
            self._token = response.json()["authentication"]["token"]
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException("token not found in response")

        try:
            self.account_id = response.json()["authentication"]["account"]["id"]
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException("account id not found in response")

    def __call__(self, r):
        """
        requests lib auth module callback
        """
        r.headers["x-aims-auth-token"] = self._token
        return r
