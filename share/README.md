# DISCLAIMER:
EARLY RELEASE, SUBJECT TO CHANGE IN THE FUTURE.

## About:

alertlogic-cli is a Command Line Client for Alertlogic services.

## Requirements:

1. python 2.7+ (3.x not supported)
1. requests library

## Installation:

The easiest way to install alertlogic-cli is using pip:

```pip install alertlogic-cli```

## Configuration:

alertlogic-cli uses a config file: `~/.alertlogic/config` and a credentials file: `~/.alertlogic/credentials`
They must be both ini style files where each section represents a profile.

Config profile can have these fields:

* `api_endpoint`: either `uk` or `us` (required)
* `account_id`: only for managed accounts, uses this account instead of user's account (uuid) (optional)
* `deployment_id`: default for deployment operations (uuid) (optional)

Credentials profile can have these fields:

* `username`: your alertlogic cloudinsight username (required)
* `password`: your alertlogic cloudinsight password (required)


Example config:

``` ini
[default]
api_endpoint = us
account_id = 123089
```

Example credentials:

``` ini
[default]
username = user@example.com
password = ultr4s3cr3t
```

## Usage

Alert Logic CLI currently supports the following commands and subcommands:

1. `deployment` - groups the deployment related operations

    Options available:

    * `--deployment_id ENVIRONMENT_ID` - to point on a customer deployment

    Operations available:

    * `set_deployment_mode` - changes deployment deployment mode between readonly or manual

        Options available:

        `--mode {readonly,automatic}` - deployment mode needed

        Example:
        ``` bash
        $ alertlogic-cli --deployment_id 00000000-0000-0000-0000-000000000000 deployment set_deployment_mode --mode readonly
        ```

    * `get_deployment_mode` - shows deployment deployment mode:

        Example:
        ``` bash
        $ alertlogic-cli --deployment_id 00000000-0000-0000-0000-000000000000 deployment get_deployment_mode
        ```

    * `get_deployment_status` - gets deployment status for a given deployment

        Example:
        ``` bash
        $ alertlogic-cli --deployment_id 00000000-0000-0000-0000-000000000000 deployment get_deployment_status
        ```

    * `list_deployed_resources` - lists security infrastructure resources deployed

        Example:
        ``` bash
        $ alertlogic-cli --deployment_id 00000000-0000-0000-0000-000000000000 deployment list_deployed_resources
        ```

    * `list_scan_queues` - lists hosts in scan queues for a given deployment

        Options available:

        `--vpc_key VPC_KEY` - filter hosts for a given VPC

        Example:
        ``` bash
        $ alertlogic-cli --deployment_id 00000000-0000-0000-0000-000000000000 deployment list_scan_queues
        ```

    * `scan_host` - puts a host in the immediate scan queue

        Options available:

        `--host_key HOST_KEY` - a host to put in the queue

        Example:
        ``` bash
        $ alertlogic-cli --deployment_id 00000000-0000-0000-0000-000000000000 deployment scan_host --host_key /aws/us-east-1/host/i-00000000000000000
        ```

For further information run `alertlogic-cli --help`.
