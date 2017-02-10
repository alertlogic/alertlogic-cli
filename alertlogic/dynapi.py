import requests
import core
import json
import logging

log = logging.getLogger(__name__)

class DynAPIException(core.AlertlogicException):
    def __init__(self, message):
        super(DynAPIException, self).__init__(core.Constants.CONTACT_MESSAGE+"dynamic api error: "+message)

class InvalidDynMethodDefinition(DynAPIException): pass
class InvalidDynMethodCall(DynAPIException): pass

class DynAPI():
    """objects of this class represent individual cloud insight services apis
    We process apidoc json metadata to dynamically generate each api method (DynMethod)"""
    def __init__(self, api_data):
        self.methods = {}
        for api_data_method in api_data:
            try:
                method = DynMethod.new_from_hash(api_data_method)
                self.methods[method.name] = method
            except InvalidDynMethodDefinition as e:
                log.debug(">> fail ({})".format(e))
                pass
    
    def set_session(self, session):
        self._session = session
    
    """This is where the magic happens, in python this function it's called every time
    a property of an object is not found, we use this functionality to return a handler
    that will in turn call the specific dynmethod, see Dynmethod.call() for more info
    """
    def __getattr__(self, name):
        def handler(*args, **kwargs):
            if name in self.methods:
                return self.methods[name].call(self._session, kwargs)
            else:
                raise InvalidDynMethodCall("dynmethod not found: {}".format(name))
        return handler

#
# DynMethod, 
#
class DynMethod():
    """A Dynmethod is made of a name, operation (http), url and a
    list of parameters, the url (DynUrl) is parsed such that fields that
    starts with ":" are treated as DynParameters
    
    The body Parameters as defined by apidocs are ignored, this processing
    will be done in the service itself"""
    @classmethod
    def new_from_hash(cls, hash):
        return cls(hash["name"].lower(), hash["type"], hash["url"], hash["parameter"]["fields"]["Parameter"])
    
    def __init__(self, name, operation, url, parameters_data):
        self.name = name.lower()
        log.debug(":: defining dynmethod: {}".format(self.name))
        
        self.operation = operation.upper()
        if self.operation not in ["GET", "POST", "DELETE", "PUT", "HEAD"]:
            raise InvalidDynMethodDefinition("invalid operation: {}".format(self.operation))
        
        url_parts = [part for part in url.lower().split("/") if len(part) > 0]
        url_parameters = {}
        body_parameters = {}
        for parameter_data in parameters_data:
            parameter = DynParameter.new_from_hash(parameter_data)
            if ":"+parameter.field in url_parts:
                url_parameters[parameter.field] = parameter
            else:
                body_parameters[parameter.field] = parameter
        
        self.url = DynUrl(url_parts, url_parameters)
        self.body = DynBody(body_parameters)
    
    """ Makes the http call by replacing the url parameters (the ones that start with ":") with
    the ones found in *input*, if *input* has a "json" field it'll be passed down to the requests lib
    """
    def call(self, session, input):
        json = None
        if "json" in input:
            json = input["json"]
            del input["json"]
        
        if "account_id" not in input:
            input["account_id"] = session.account
        
        parsed_url = session.api_url + self.url.parse(input)
        log.debug("calling: {} {}".format(self.operation, parsed_url))
        return requests.request(self.operation, parsed_url, json=json, auth=session)

class DynBody():
    def __init__(self, parameters):
        self.parameters = parameters

class DynUrl():
    """ Splits a url in parts of 2 types:
    * string: simple strings, nothing special here
    * dynparameters:
    e.g:
        /sources/:account_id/source/:source_id
        "sources" and "source" are both strings
        ":account_id" and "source_id" are dynparameters, if you want to parse this url
        you must include these two in *input*
    """
    def __init__(self, parts, parameters):
        self.parameters = parameters
        self.parts = []
        for part in parts:
            if part[0] == ":":
                field = part[1:]
                if field in self.parameters:
                    self.parts.append(self.parameters[field])
                else:
                    raise InvalidDynMethodDefinition("missing url parameter definition {}".format(field))
            else:
                self.parts.append(part)
    
    def parse(self, input):
        result = ""
        for part in self.parts:
            # replace with input[] if dynparameter, otherwise use the raw string
            if isinstance(part, DynParameter):
                if part.field in input:
                    result += "/"+input[part.field]
                else:
                    raise InvalidDynMethodCall("missing url input parameter {}".format(part.field))
            else:
                result += "/"+part
        return result

class DynParameter():
    @classmethod
    def new_from_hash(cls, hash):
        return cls(hash["field"], hash["type"], hash["optional"])
    
    def __init__(self, field, type, optional):
        self.field = field
        self.type = type
        self.optional = optional


#
# Globals:
#
def load(session=None):
    """parse apidoc jsons files found in API_DATA_DIR
    each file will be mapped out into a DynAPI global object capable
    of querying each service
    e.g:
      dynapi.load(session)
      dynapi.sources.merge_source(id=environment_id, json=new_config)
    """
    global sources
    
    with open(core.Constants.API_DATA_DIR+"/sources.json") as api_data_json:
        api_data = json.load(api_data_json)
        sources = DynAPI(api_data)
        if session:
            sources.set_session(session)
