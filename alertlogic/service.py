import requests

class InvalidEndpointCall(Exception):
    pass


class Service:

    def __init__(self, name, version='v1', session=None):
        self.name=name
        self.set_session(session)
        self.version=version

    def set_session(self, session):
        """ changes current session, this session object is used to authenticate
         api calls
        :param session: an authenticated alertlogic.auth.Session object
        """
        self._session = session

    def call_endpoint(self, method, path_parts, params=None, json=None):
        url = self.build_url(path_parts)
        try:
            return requests.request(method, url, params=params, json=json, auth=self._session)
        except requests.exceptions.HTTPError as e:
            raise InvalidEndpointCall(e.message)

    def build_url(self, path_parts):
        path = "/".join([self.name, self.version] + path_parts)
        return self._session.region.get_api_endpoint() + '/' + path
