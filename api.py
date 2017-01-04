import ConfigParser
import requests
import IPython

class Config():
    def __init__(self, filename):
        self._filename = filename
        self._parser = ConfigParser.ConfigParser()
        self._parser.read(self._filename)
        self.set_profile("default")
    
    def set_profile(self, profile):
        self.username = self._parser.get(profile, "username")
        self.password = self._parser.get(profile, "password")
        self.datacenter = self._parser.get(profile, "datacenter")
        self.api_url = self._get_api_url(self.datacenter)
    
    def _get_api_url(self, datacenter):
        if datacenter == "dev":
            return "https://api.product.dev.alertlogic.com"
        elif datacenter == "us":
            return "https://api.cloudinsight.alertlogic.com"

class ALAuth():
    def __init__(self, api_url, username, password):
        self.api_url = api_url
        auth = requests.auth.HTTPBasicAuth(username, password)
        response = requests.post(self.api_url+"/aims/v1/authenticate", auth=auth)
        self._token = response.json()["authentication"]["token"]
    
    def __call__(self, r):
        r.headers["x-aims-auth-token"] = self._token
        return r

class SourcesAPI():
    def __init__(self, auth):
        self.auth = auth
        self.api_url = self.auth.api_url+"/sources/v1/"
    
    def url(self, *parts):
        return self.api_url + ( "/".join(str(part) for part in parts) )
    
    def get_source_type(self, account_id, source_id):
        response = requests.get(self.url(account_id, "sources", source_id), auth=self.auth)
        return response.json()["source"]["type"]
    
    def update_source(self, account_id, source_id, changes):
        response = requests.post(self.url(account_id, "sources", source_id), json=changes, auth=self.auth)
        return response.ok
    
    def set_environment_deployment_mode(self, account_id, environment_id, mode):
        if self.get_source_type(account_id, environment_id) == "environment":
            new_config = { "source": { "config": { "deployment_mode": mode } } }
            return self.update_source(account_id, environment_id, new_config)
 
config = Config("/home/juan/pyclient/config")
auth = ALAuth(config.api_url, config.username, config.password)
sources_api = SourcesAPI(auth)
