import ConfigParser
import logging

import alertlogic.auth

log = logging.getLogger()


class CredentialsException(Exception):
    def __init__(self, message):
        super(CredentialsException, self).__init__("credentials error: {}".format(message))


class Credentials():
    """
    Reads and stores username and passwords, creates session objects with those fields
    Current issues with password data we haven't addressed them because
    there's no portable way to do it:
    * it's only delete()d meaning the data will be there until gc is triggered
    * it's never zeroed
    """

    def __init__(self, filename, profile):
        self._parser = ConfigParser.ConfigParser()
        self._read(filename)
        self._set_profile(profile)

    def make_session(self, region):
        session = alertlogic.auth.Session(region, self._username, self._password)
        del (self._password)
        return session

    def _read(self, filename):
        try:
            read_ok = self._parser.read(filename)
            if filename not in read_ok:
                raise CredentialsException("unable to read {}".format(filename))
        except ConfigParser.MissingSectionHeaderError:
            raise CredentialsException("invalid format")

    def _set_profile(self, profile):
        try:
            self._username = self._parser.get(profile, "username")
            self._password = self._parser.get(profile, "password")
        except ConfigParser.NoSectionError as e:
            raise CredentialsException("credentials profile {} not found".format(profile))
        except ConfigParser.NoOptionError as e:
            raise CredentialsException("credentials field {} not found in profile {}".format(e.option, profile))
