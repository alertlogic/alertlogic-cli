import dynapi
import core

import requests

class InvalidParameterException(core.AlertlogicException):
    def __init__(self, name, value, problem):
        super(InvalidParameterException, self).__init__("{}[ {} ] {}".format(name, value, problem))

class InvalidAPIHTTPResponse(core.AlertlogicException):
    def __init__(self, trying_to, message):
        super(InvalidAPIHTTPResponse, self).__init__("{} while trying to {}".format(message, trying_to))

class InvalidAPIResponse(core.AlertlogicException):
    def __init__(self, trying_to, cause, response):
        msg = "{} while trying to {} code[ {} ] content[ {} ]".format(cause, trying_to, response.status_code, response.content)
        super(InvalidAPIResponse, self).__init__(msg)

class DeploymentMode():
    @classmethod
    def set(cls, environment_id, mode):
        try:
            response = dynapi.sources.get_source(id=environment_id)
            if response.status_code == 404:
                raise InvalidParameterException("environment", environment_id, "not found")
            if response.json()["source"]["type"] != "environment":
                raise InvalidParameterException("environment", environment_id, "is not an environment")
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidAPIHTTPResponse("validate environment", e.message)
        except KeyError:
            raise InvalidAPIResponse("validate environment", "source.type not found", response)
        
        try:
            new_config = { "source": { "config": { "deployment_mode": mode } } }
            response = dynapi.sources.merge_source(id=environment_id, json=new_config)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidAPIHTTPResponse("update deployment mode", e.message)
        
        return True
