import os.path
import ConfigParser
import logging

import alertlogic.auth

log = logging.getLogger()

DEFAULT_CONFIG_FILE = os.path.expanduser("~/.alertlogic/config.ini")

class ConfigException(Exception):
    def __init__(self, message):
        super(ConfigException, self).__init__("configuration error: {}".format(message))

class Config():
    def __init__(self, config_file=DEFAULT_CONFIG_FILE, profile="default"):
        self.read(config_file)
        self.set_profile(profile)

    def make_session(self):
        session = alertlogic.auth.Session(self.api_endpoint, self.username, self.password, self.account_id)
        return session

    def read(self, config_file):
        try:
            self._parser = ConfigParser.ConfigParser()
            read_ok = self._parser.read(config_file)
            if not config_file in read_ok:
                raise ConfigException("unable to read {}".format(config_file))
        except ConfigParser.MissingSectionHeaderError:
            raise ConfigException("invalid format")

    def set_profile(self, profile):
        try:
            self.username = self._parser.get(profile, "username")
            self.password = self._parser.get(profile, "password")
            self.api_endpoint = self._parser.get(profile, "api_endpoint")

            self.account_id = None
            self.environment_id = None

            if self._parser.has_option(profile, "environment_id"):
                self.environment_id = self._parser.get(profile, "environment_id")
                log.debug("found environment_id: {} option in config file".format(self.environment_id))

        except ConfigParser.NoSectionError as e:
            raise ConfigException("profile {} not found".format(profile))
        except ConfigParser.NoOptionError as e:
            raise ConfigException("option {} not found in profile {}".format(e.option, profile))
