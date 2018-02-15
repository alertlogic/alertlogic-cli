import os.path
import ConfigParser
import logging

import alertlogic.auth

log = logging.getLogger()


class ConfigException(Exception):
    def __init__(self, message):
        super(ConfigException, self).__init__("config error: {}".format(message))


class Config():
    """
    Reads and stores configuration parameters
    """

    def __init__(self, filename, profile):
        self._parser = ConfigParser.ConfigParser()
        self._read(filename)
        self._set_profile(profile)

    def _read(self, filename):
        try:
            read_ok = self._parser.read(filename)
            if filename not in read_ok:
                raise ConfigException("unable to read {}".format(filename))
        except ConfigParser.MissingSectionHeaderError:
            raise ConfigException("invalid format in file {}".format(filename))

    def _set_profile(self, profile):
        self.api_endpoint = None
        self.account_id = None
        self.deployment_id = None

        try:
            self.api_endpoint = self._parser.get(profile, "api_endpoint")
        except ConfigParser.NoSectionError as e:
            raise ConfigException("profile {} not found".format(profile))
        except ConfigParser.NoOptionError as e:
            raise ConfigException("option {} not found in profile {}".format(e.option, profile))

        if self._parser.has_option(profile, "account_id"):
            self.account_id = self._parser.get(profile, "account_id")
            log.debug("found account_id: {} option in config file".format(self.account_id))

        if self._parser.has_option(profile, "deployment_id"):
            self.deployment_id = self._parser.get(profile, "deployment_id")
            log.debug("found deployment_id: {} option in config file".format(self.deployment_id))
