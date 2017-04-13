# -*- coding: utf-8 -*-
"""
    alertlogic.auth
    ~~~~~~~~~~~~~~
    alertlogic authentication/authorization
"""

import requests

API_ENDPOINTS = {
    "us": "https://api.cloudinsight.alertlogic.com",
    "uk": "https://api.cloudinsight.alertlogic.co.uk",
    "integration": "https://api.product.dev.alertlogic.com"
}

class AuthenticationException(Exception):
    def __init__(self, message):
        super(AuthenticationException, self).__init__("authentication error: {}".format(message))

class Session():
    """Authenticates against alertlogic aims service and stores session information (token and account id),
    additionally objects of this class can be used as auth modules for requests, more info:
    http://docs.python-requests.org/en/master/user/authentication/#new-forms-of-authentication
    """
    def __init__(self, api_endpoint, username, password, account_id):
        """
        :param api_endpoint: either "uk" or "us" or any api endpoint url
        :param username: your alertlogic cloudinsight username
        :param password: your alertlogic cloudinsight password
        """
        if api_endpoint in API_ENDPOINTS:
            self.api_endpoint = API_ENDPOINTS[api_endpoint]
        else:
            self.api_endpoint = api_endpoint
        self.account_id = account_id
        self._authenticate(username, password)

    def _authenticate(self, username, password):
        """Authenticates against alertlogic Access and Identity Management Service (AIMS)
        more info: https://console.cloudinsight.alertlogic.com/api/aims/#api-AIMS_Authentication_and_Authorization_Resources-Authenticate
        """
        try:
            auth = requests.auth.HTTPBasicAuth(username, password)
            response = requests.post(self.api_endpoint+"/aims/v1/authenticate", auth=auth)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise AuthenticationException("invalid http response {}".format(e.message))

        try:
            self._token = response.json()["authentication"]["token"]
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException("token not found in response")

        try:
            if not self.account_id:
                self.account_id = response.json()["authentication"]["account"]["id"]
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException("account id not found in response")

    def __call__(self, r):
        """ requests auth module callback
        """
        r.headers["x-aims-auth-token"] = self._token
        return r
