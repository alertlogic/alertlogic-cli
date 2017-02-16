import core
import dynapi

import requests

class InvalidParameterException(core.AlertlogicException):
    def __init__(self, name, value, problem):
        super(InvalidParameterException, self).__init__("{} \"{}\" {}".format(name, value, problem))

class InvalidAPIHTTPResponse(core.AlertlogicException):
    def __init__(self, trying_to, message):
        super(InvalidAPIHTTPResponse, self).__init__("{} while trying to {}".format(message, trying_to))

class InvalidAPIResponse(core.AlertlogicException):
    def __init__(self, trying_to, cause, response):
        raw = "{} while trying to {} code[ {} ] content[ {} ]"
        msg = raw.format(cause, trying_to, response.status_code, response.content)
        super(InvalidAPIResponse, self).__init__(msg)

class Commands():
    def __init__(self, services):
        self.services = services
    
    def validate_environment(self, environment_id):
        try:
            response = self.services.sources.get_source(id=environment_id)
            if response.status_code == 404:
                raise InvalidParameterException("environment", environment_id, "not found")
            response.raise_for_status()
            if response.json()["source"]["type"] != "environment":
                raise InvalidParameterException("environment", environment_id, "is not an environment")
        except requests.exceptions.HTTPError as e:
            raise InvalidAPIHTTPResponse("validate environment", e.message)
        except (KeyError, ValueError):
            raise InvalidAPIResponse("validate environment", "source.type not found", response)
        
        return response

    def environment_set_deployment_mode(self, environment_id, mode):
        response = self.validate_environment(environment_id)
        try:
            new_config = { "source": { "config": { "deployment_mode": mode } } }
            response = self.services.sources.merge_source(id=environment_id, json=new_config)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidAPIHTTPResponse("update deployment mode", e.message)
        
        return "ok"
    
    def environment_get_deployment_mode(self, environment_id):
        response = self.validate_environment(environment_id)
        try:
            mode = response.json()["source"]["config"]["deployment_mode"]
            if mode == "readonly":
                return "readonly"
            else:
                return "automatic"
        except KeyError: # json parsed but can't find specific field
            return "automatic"
