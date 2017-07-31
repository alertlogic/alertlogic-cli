import alertlogiccli.config
import alertlogiccli.credentials
import alertlogic.region
import alertlogic.auth
import alertlogic.dynapi

class Context():
    """
    Internally stores commands context objects including:
    * command line arguments
    * dynapi services
    * configuration
    * credentials
    * region
    * session
    
    It mixes these objects and exposes only two things:
    * authenticated services api
    * final arguments dict by mixing data from config, cli arguments and session
    """
    def __init__(self, args, config, credentials):
        self._args = args
        self._config = config
        self._credentials = credentials
        
        api_endpoint = self._args.api_endpoint or self._config.api_endpoint
        self._region = alertlogic.region.Region(api_endpoint)
        
        self._session = self._credentials.make_session(self._region)
        self._services = alertlogic.dynapi.Services()
        self._services.set_session(self._session)
    
    def get_services(self):
        return self._services
    
    def get_final_args(self):
        all_args = vars(self._args).copy()
        for key in ["command", "profile", "api_endpoint",
                    "config_file", "credentials_file", "logging_config_file"]:
            
            try:
                del(all_args[key])
            except KeyError:
                continue
        
        all_args["account_id"] = self._args.account_id or self._config.account_id or self._session.account_id
        all_args["deployment_id"] = self._args.deployment_id or self._config.deployment_id
        return all_args