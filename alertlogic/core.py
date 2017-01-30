import ConfigParser
import requests
import os.path

class AlertlogicException(Exception): pass

class ConfigException(AlertlogicException):
    def __init__(self, message):
        super(ConfigException, self).__init__("config file {} error: {}".format(Constants.CONFIG_FILE, message))

class AuthenticationException(AlertlogicException):
    def __init__(self, message):
        super(AuthenticationException, self).__init__("authentication error: {}".format(message))

class Constants():
    CONTACT_MESSAGE = (
        "Oops something went wrong.\n",
        "Please contact support@alertlogic.com and provide the following information:\n"
    )
    CONFIG_FILE = os.path.expanduser("~/.alertlogic/config")
    API_DATA_DIR = os.path.abspath(os.path.dirname(__file__)+"/../api_data")
    DCS = {
        "dev": "https://api.product.dev.alertlogic.com",
        "us": "https://api.cloudinsight.alertlogic.com",
        "uk": "https://api.cloudinsight.alertlogic.co.uk"
    }    

class Config():
    def __init__(self, profile="default"):
        self.read()
        self.set_profile(profile)
    
    def read(self):
        try:
            self._parser = ConfigParser.ConfigParser()
            read_ok = self._parser.read(Constants.CONFIG_FILE)
            if not Constants.CONFIG_FILE in read_ok:
                raise ConfigException("unable to read")
        except ConfigParser.MissingSectionHeaderError:
            raise ConfigException("invalid format")
    
    def set_profile(self, profile):
        try:
            self.username = self._parser.get(profile, "username")
            self.password = self._parser.get(profile, "password")
            self.datacenter = self._parser.get(profile, "datacenter")
            
            if not self.datacenter in Constants.DCS:
                raise ConfigException("invalid datacenter {} in profile {}".format(self.datacenter, profile))
            
            if self._parser.has_option(profile, "account"):
                self.account = self._parser.get(profile, "account")
            else:
                self.account = None
        except ConfigParser.NoSectionError as e:
            raise ConfigException("profile {} not found".format(profile))
        except ConfigParser.NoOptionError as e:
            raise ConfigException("option {} not found in profile {}".format(e.option, profile))

class Session():
    def __init__(self, config):
        self._config = config
        self.api_url = Constants.DCS[self._config.datacenter]
        self.authenticate()
    
    def authenticate(self):
        try:
            auth = requests.auth.HTTPBasicAuth(self._config.username, self._config.password)
            response = requests.post(self.api_url+"/aims/v1/authenticate", auth=auth)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise AuthenticationException("invalid http response {}".format(e.message))
        
        try:
            self._token = response.json()["authentication"]["token"]
        except KeyError:
            raise AuthenticationException("token not found in response")
        
        try:
            self.user_account = response.json()["authentication"]["account"]["id"]
            self.account = self._config.account if self._config.account else self.user_account
        except KeyError:
            raise AuthenticationException("account id not found in response")
    
    def __call__(self, r):
        r.headers["x-aims-auth-token"] = self._token
        return r
