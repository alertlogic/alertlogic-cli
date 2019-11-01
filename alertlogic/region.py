# -*- coding: utf-8 -*-
"""
    alertlogic.region
    ~~~~~~~~~~~~~~
    alertlogic region management
"""
"""
List of known regions
"""
REGIONS = {
    "us": "https://api.cloudinsight.alertlogic.com",
    "uk": "https://api.cloudinsight.alertlogic.co.uk"
}


class Region():
    """
    Abstracts an alertlogic region, for now it only represents the api endpoint url
    """

    def __init__(self, api_endpoint, auth_endpoint=None):
        """
        :param api_endpint: either a region ("us" or "uk") or an insight api url
        """
        if auth_endpoint is None:
            auth_endpoint = api_endpoint
        self._api_endpoint = api_endpoint
        self._auth_endpoint = auth_endpoint

    def get_api_endpoint(self):
        """
        returns the region's api endpoint url
        """
        if self._api_endpoint in REGIONS:
            return REGIONS[self._api_endpoint]
        else:
            return self._api_endpoint

    def get_auth_endpoint(self):
        """
        returns the region's api endpoint url
        """
        if self._api_endpoint in REGIONS:
            return REGIONS[self._auth_endpoint]
        else:
            return self._auth_endpoint
