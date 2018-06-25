from service import Service


class Otis(Service):

    def __init__(self, session):
        Service.__init__(self, "otis", "v2", session)

    def write_option(self, account_id, option_name, option_scope, option_value):
        option = {
            "name": option_name,
            "scope": option_scope,
            "value": option_value
        }
        return self.post([account_id, 'options'], json=option)

    def get_options(self, account_id):
        return self.get([account_id, 'options'])

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
        return self.get([account_id, 'sources', source_id])

    def get_deployment_mode(self, account_id, deployment_id):
        response = self.get_source(account_id, deployment_id)
        try:
            mode = response.json()["source"]["config"]["deployment_mode"]
            return mode
        except KeyError:
            raise KeyError

    def merge_sources(self, account_id, source_id, source):
        return self.post([account_id, 'sources', source_id], json=source)

    def set_mode(self, account_id, deployment_id, mode):
        source = {
            "source": {
                "config": {
                    "deployment_mode": mode
                }
            }
         }
        return self.merge_sources(account_id, deployment_id, source)

    def set_deployment_scope(self, account_id, source_id, include, exclude):
        source = {
            "source": {
                "config": {
                    "aws": {
                        "scope": {
                            "include": include,
                            "exclude": exclude
                        }
                    }
                }
            }
        }
        return self.merge_sources(account_id, source_id, source)

    def create_deployment(self, account_id, aws_account_id, credential_id, name, mode, scan=True):
        source = {
            "source": {
                "config": {
                    "collection_method": "api",
                    "collection_type": "aws",
                    "aws": {
                        "account_id": aws_account_id,
                        "credential": {
                            "id": credential_id
                        },
                        "discover": True,
                        "scan": scan,
                        "deployment_mode": mode
                    }
                },
                "enabled": True,
                "name": name,
                "product_type": "outcomes",
                "tags": [],
                "type": "environment"
            }
        }
        return self.post([account_id, 'sources'], json=source)

    def delete_source(self, account_id, source_id):
        return self.delete([account_id, 'sources', source_id])


class Launcher(Service):

    def __init__(self, session):
        Service.__init__(self, "launcher", "v1", session)

    def list_deployed(self, account_id, deployment_id):
        return self.get([account_id, deployment_id, 'resources'])

    def deployment_status(self, account_id, deployment_id):
        return self.get([account_id, 'environments', deployment_id])


class ScanScheduler(Service):

    def __init__(self, session):
        Service.__init__(self, "scheduler", "v1", session)

    def scan_host(self, account_id, deployment_id, asset_key):
        params = {'asset': asset_key}
        return self.put([account_id, deployment_id, 'scan'], query_params=params)

    def list_scan_assets(self, account_id, deployment_id):
        return self.get([account_id, deployment_id, 'list'])

    def get_scan_summary(self, account_id, deployment_id, vpc_key=None):
        if vpc_key:
            params = {"vpc_key": vpc_key}
        else:
            params = {}
        return self.get([account_id, deployment_id, 'summary'], query_params=params)


class Saturn(Service):

    def __init__(self, session):
        Service.__init__(self, "saturn", "v1", session)

    def redeploy(self, account_id, deployment_id=None, vpc_key=None):
        if deployment_id and vpc_key:
            params = {'deployment_id': deployment_id, 'vpc_key': vpc_key}
        elif vpc_key is None and deployment_id is not None:
            params = {'deployment_id': deployment_id}
        else:
            params = None
        return self.post([account_id, 'redeploy'], query_params=params)

    def deployed_installations(self, account_id, vpc_key=None):
        if vpc_key is None:
            params = None
        else:
            params = {'vpc_key': vpc_key}
        return self.get([account_id, 'installations'], params)


class Skaletor(Service):

    def __init__(self, session):
        Service.__init__(self, "skaletor", "v1", session)

    def get_scanner_estimation(self, account_id, deployment_id=None, vpc_key=None):
        if vpc_key is not None and deployment_id is not None:
            params = {'deployment_id': deployment_id, 'vpc_key': vpc_key}
        elif vpc_key is None and deployment_id is not None:
            params = {'deployment_id': deployment_id}
        elif vpc_key is not None and deployment_id is None:
            params = {'vpc_key': vpc_key}
        else:
            params = None
        return self.get([account_id, 'scanners'], query_params=params)


class Credentials(Service):

    def __init__(self, session):
        Service.__init__(self, "credentials", "v2", session)

    def create_credential(self, account_id, name, arn):
        json = {
            "name": name,
            "secrets": {
                "type": "aws_iam_role",
                "arn": arn
            }
        }
        return self.post([account_id, 'credentials'], json=json)

    def delete_credential(self, account_id, credential_id):
        return self.delete([account_id, 'credentials', credential_id])


class Themis(Service):

    def __init__(self, session):
        Service.__init__(self, "themis", "v1", session)

    def get_role(self, account_id, platform_type, role_type, role_version):
        return self.get([account_id, "roles", platform_type, role_type, role_version])

    def validate_credentials(self, account_id, platform_type, role_type, version, arn):
        role = {
            "platform_type": platform_type,
            "role_type": role_type,
            "role_version": version,
            "arn": arn,
            "external_id": account_id
        }
        return self.post(['validate', platform_type, role_type], json=role)


class ScanCollect(Service):

    def __init__(self, session):
        Service.__init__(self, "scancollect", "v1_remediation", session)

    def get_appliance_vmserver_id(self, account_id, deployment_id, appliance_id):
        return self.get([account_id, deployment_id, 'appliance_vmserver_id', appliance_id])


class AssetsQuery(Service):

    def __init__(self, session):
        Service.__init__(self, "assets_query", "v1", session)

    def get_assets_in_deployment(self, account_id, deployment_id, params=None):
        return self.get([account_id, 'deployments', deployment_id, 'assets'], query_params=params)


class Deployments(Service):

    def __init__(self, session):
        Service.__init__(self, "deployments", "v1", session)

    def create_deployment(self, account_id, deployment_json):
        return self.post([account_id, "deployments"], json=deployment_json)

    def delete_deployment(self, account_id, deployment_id):
        return self.delete([account_id, "deployments", deployment_id])

    def get_deployment(self, account_id, deployment_id):
        return self.get([account_id, "deployments", deployment_id])

    def list_deployments(self, account_id):
        return self.get([account_id, "deployments"])

    def update_deployment(self, account_id, deployment_id, deployment_json):
        return self.put([account_id, "deployments", deployment_id], json=deployment_json)