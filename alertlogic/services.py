from service import Service


class Otis(Service):

    def __init__(self, session):
        Service.__init__(self, "otis", "v2", session)

    def write_option(self, account_id, option_name, option_scope, option_value):
        path_parts = [account_id, 'options']
        option = {
            "name": option_name,
            "scope": option_scope,
            "value": option_value
        }
        return self.call_endpoint('POST', path_parts, json=option)

    def get_options(self, account_id):
        path_parts = [account_id, 'options']
        return self.call_endpoint('GET', path_parts)

    def set_subnet(self, account_id, provider_id, provider_type, vpc_id, subnet_id):
        option_scope = {
            "provider_id": provider_id,
            "provider_type": provider_type,
            "vpc_id": vpc_id
        }
        return self.write_option(account_id, "predefined_security_subnet", option_scope, subnet_id)


class Sources(Service):

    def __init__(self, session):
        Service.__init__(self, "sources", "v1", session)

    def get_source(self, account_id, source_id):
        path_parts = [account_id, 'sources', source_id]
        return self.call_endpoint('GET', path_parts)

    def get_deployment_mode(self, account_id, deployment_id):
        response = self.get_source(account_id, deployment_id)
        try:
            mode = response.json()["source"]["config"]["deployment_mode"]
            return mode
        except KeyError:
            raise KeyError

    def set_mode(self, account_id, deployment_id, mode):
        path_parts = [account_id, 'sources', deployment_id]
        source = {
            "source": {
                "config": {
                    "deployment_mode": mode
                }
            }
        }
        return self.call_endpoint('POST', path_parts, json=source)


class Launcher(Service):

    def __init__(self, session):
        Service.__init__(self, "launcher", "v1", session)

    def list_deployed(self, account_id, deployment_id):
        path_parts = [account_id, deployment_id, 'resources']
        return self.call_endpoint('GET', path_parts)

    def deployment_status(self, account_id, deployment_id):
        path_parts = [account_id, 'environments', deployment_id]
        return self.call_endpoint('GET', path_parts)


class ScanScheduler(Service):

    def __init__(self, session):
        Service.__init__(self, "scheduler", "v1", session)

    def scan_host(self, account_id, deployment_id, asset_key):
        path_parts = [account_id, deployment_id, 'scan']
        params = {'asset': asset_key}
        return self.call_endpoint('PUT', path_parts, params=params)

    def list_scan_assets(self, account_id, deployment_id):
        path_parts = [account_id, deployment_id, 'list']
        return self.call_endpoint('GET', path_parts)


class Saturn(Service):

    def __init__(self, session):
        Service.__init__(self, "saturn", "v1", session)

    def redeploy(self, account_id, deployment_id=None, vpc_key=None):
        path_parts = [account_id, 'redeploy']
        if deployment_id and vpc_key:
            params = {'deployment_id': deployment_id, 'vpc_key': vpc_key}
        elif vpc_key is None and deployment_id is not None:
            params = {'deployment_id': deployment_id}
        else:
            params = None
        return self.call_endpoint('POST', path_parts, params=params)

    def deployed_installations(self, account_id, vpc_key=None):
        path_parts = [account_id, 'installations']
        if vpc_key is None:
            params = None
        else:
            params = {'vpc_key': vpc_key}
        return self.call_endpoint('GET', path_parts, params)


class Skaletor(Service):

    def __init__(self, session):
        Service.__init__(self, "skaletor", "v1", session)

    def get_scanner_estimation(self, account_id, deployment_id=None, vpc_key=None):
        path_parts = [account_id, 'scanners']
        if vpc_key is not None and deployment_id is not None:
            params = {'deployment_id': deployment_id, 'vpc_key': vpc_key}
        elif vpc_key is None and deployment_id is not None:
            params = {'deployment_id': deployment_id}
        elif vpc_key is not None and deployment_id is None:
            params = {'vpc_key': vpc_key}
        else:
            params = None
        return self.call_endpoint('GET', path_parts, params=params)


class Credentials(Service):

    def __init__(self, session):
        Service.__init__(self, "credentials", "v2", session)

    def create_credential(self, account_id, name, arn):
        path_parts = [account_id, 'credentials']
        json = {
            "name": name,
            "secrets": {
                "type": "aws_iam_role",
                "arn": arn
            }
        }
        return self.call_endpoint('POST', path_parts, json=json)

    def delete_credential(self, account_id, credential_id):
        path_parts = [account_id, 'credentials', credential_id]
        return self.call_endpoint('DELETE', path_parts)


class Themis(Service):

    def __init__(self, session):
        Service.__init__(self, "themis", "v1", session)

    def get_role(self, account_id, playform_type, role_type, role_version):
        path_parts = [account_id, playform_type, role_type, role_version]
        return self.call_endpoint('GET', path_parts)

    def validate_credentials(self, account_id, platform_type, role_type, version, arn):
        path_parts = ['validate', platform_type, role_type]
        role = {
            "platform_type": platform_type,
            "role_type": role_type,
            "role_version": version,
            "arn": arn,
            "external_id": account_id
        }
        return self.call_endpoint('POST', path_parts, json=role)