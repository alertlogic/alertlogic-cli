import os.path
import ConfigParser
import logging

import alertlogic.auth

log = logging.getLogger(__name__)

DEFAULT_CONFIG_FILE = os.path.expanduser("~/.alertlogic/config")

class ConfigException(Exception):
    def __init__(self, message):
        super(ConfigException, self).__init__("config file {} error: {}".format(DEFAULT_CONFIG_FILE, message))

class Config():
    def __init__(self, profile="default"):
        self.read()
        self.set_profile(profile)
    
    def make_session(self):
        session = alertlogic.auth.Session(self.api_endpoint, self.username, self.password)
        return session
    
    def read(self):
        try:
            self._parser = ConfigParser.ConfigParser()
            read_ok = self._parser.read(DEFAULT_CONFIG_FILE)
            if not DEFAULT_CONFIG_FILE in read_ok:
                raise ConfigException("unable to read")
        except ConfigParser.MissingSectionHeaderError:
            raise ConfigException("invalid format")
    
    def set_profile(self, profile):
        try:
            self.username = self._parser.get(profile, "username")
            self.password = self._parser.get(profile, "password")
            self.api_endpoint = self._parser.get(profile, "api_endpoint")
            
            if self._parser.has_option(profile, "account"):
                self.account = self._parser.get(profile, "account")
                log.debug("found account_id {} override in config file".format(self.account))
            else:
                self.account = None
        except ConfigParser.NoSectionError as e:
            raise ConfigException("profile {} not found".format(profile))
        except ConfigParser.NoOptionError as e:
            raise ConfigException("option {} not found in profile {}".format(e.option, profile))
