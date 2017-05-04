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

alertlogic-cli uses only a single config file: `~/.alertlogic/config.ini`.
It must be an ini style file where each section represents a profile.
Each profile has 3 fields:

* `username`: your alertlogic's username (the one you use to login on alertlogic's web portal)
* `password`: your alertlogic's password (same as above)
* `datacenter`: either `uk` or `us`

Example:

``` ini
[default]
username = user@example.com
password = editme
datacenter = us
```

## Usage

Alert Logic CLI currently supports the following commands and subcommands:

1. `environment` - groups the environment related operations

    Options available:

    * `--environment_id ENVIRONMENT_ID` - to point on a customer environment

    Operations available:

    * `set_deployment_mode` - changes environment deployment mode between readonly or manual

        Options available:

        `--mode {readonly,automatic}` - deployment mode needed

        Example:
        ``` bash
        $ alertlogic-cli environment --environment_id 00000000-0000-0000-0000-000000000000 set_deployment_mode --mode readonly
        ```

    * `get_deployment_mode` - shows environment deployment mode:

        Example:
        ``` bash
        $ alertlogic-cli environment --environment_id 00000000-0000-0000-0000-000000000000 get_deployment_mode
        ```

    * `get_deployment_status` - gets deployment status for a given environment

        Example:
        ``` bash
        $ alertlogic-cli environment --environment_id 00000000-0000-0000-0000-000000000000 get_deployment_status
        ```

    * `list_deployed_resources` - lists security infrastructure resources deployed

        Example:
        ``` bash
        $ alertlogic-cli environment --environment_id 00000000-0000-0000-0000-000000000000 list_deployed_resources
        ```

    * `list_scan_queues` - lists hosts in scan queues for a given environment

        Options available:

        `--vpc_key VPC_KEY` - filter hosts for a given VPC

        Example:
        ``` bash
        $ alertlogic-cli environment --environment_id 00000000-0000-0000-0000-000000000000 list_scan_queues
        ```

    * `scan_host` - puts a host in the immediate scan queue

        Options available:

        `--host_key HOST_KEY` - a host to put in the queue

        Example:
        ``` bash
        $ alertlogic-cli environment --environment_id 00000000-0000-0000-0000-000000000000 scan_host --host_key /aws/us-east-1/host/i-00000000000000000
        ```

For further information run `alertlogic-cli --help`.
