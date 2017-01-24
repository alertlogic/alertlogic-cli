#! /usr/bin/env python2

#https://console.product.dev.alertlogic.com/api/sources/api_data.json

import IPython

import ConfigParser
import requests
import json

class InvalidDynMethodDefinition(Exception): pass
class InvalidDynMethodCall(Exception): pass

class ALAuth():
    def __init__(self, api_url, username, password):
        self.api_url = api_url
        auth = requests.auth.HTTPBasicAuth(username, password)
        response = requests.post(self.api_url+"/aims/v1/authenticate", auth=auth)
        self._token = response.json()["authentication"]["token"]
    
    def __call__(self, r):
        r.headers["x-aims-auth-token"] = self._token
        return r

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

class DynAPI():
    def __init__(self, auth, api_url, api_data):
        self.auth = auth
        self.api_url = api_url
        self.methods = {}
        for api_data_method in api_data:
            try:
                method = DynMethod.new_from_hash(api_data_method)
                self.methods[method.name] = method
            except InvalidDynMethodDefinition as e:
                print(">> fail ({})".format(e))
            
    def __getattr__(self, name):
        def handler(*args, **kwargs):
            if name in self.methods:
                return self.methods[name].call(self.auth, self.api_url, kwargs)
            else:
                raise InvalidDynMethodCall("DynMethod not found: {}".format(name))
        return handler

class DynMethod():
    @classmethod
    def new_from_hash(cls, hash):
        return cls(hash["name"].lower(), hash["type"], hash["url"], hash["parameter"]["fields"]["Parameter"])
    
    def __init__(self, name, operation, url, parameters_data):
        self.name = name.lower()
        print ":: defining dynmethod: {}".format(self.name)
        
        self.operation = operation.upper()
        #TODO: should we handle multiple ops? (e.g "get/post/delete")
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
    
    def call(self, auth, api_url, input):
        if "json" in input:
            json = input["json"]
            del input["json"]
        else:
            json = None
        parsed_url = api_url + self.url.parse(input)
        print("calling: {} {}".format(self.operation, parsed_url))
        return requests.request(self.operation, parsed_url, json=json, auth=auth)
        
class DynBody():
    def __init__(self, parameters):
        self.parameters = parameters

class DynUrl():
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
        print "  -> dynparameter: {}".format(self.field)
    
    def validate(self, value):
        if self.type == "string":
            return True
        else:
            return False

class APIS():
    sources = None
    
    @classmethod
    def load(cls):
        config = Config("/home/juan/al/cds/alcli-prototype/config")
        auth = ALAuth(config.api_url, config.username, config.password)
        
        with open("api_data.json") as api_data_json:
            api_data = json.load(api_data_json)
            cls.sources = DynAPI(auth, config.api_url, api_data)

class DeploymentMode():
    @classmethod
    def set(cls, account_id, environment_id, mode):
        source_type = APIS.sources.get_source(account_id=account_id, id=environment_id).json()["source"]["type"]
        if source_type == "environment":
            new_config = { "source": { "config": { "deployment_mode": mode } } }
            response = APIS.sources.merge_source(account_id=account_id, id=environment_id, json=new_config)
            return response.ok
