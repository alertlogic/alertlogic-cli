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

alertlogic-cli uses only a single config file: `~/.alertlogic/config`.
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

alertlogic-cli currently supports the following commands and subcommands:

### `environment`:
    * `set_deployment_mode`: for a given environment changes deployment mode between readonly or manual, usage:
    ``` set_deployment_mode <environment_id> <readonly|manual>```, example:
    ``` bash
    $ alertlogic-cli environment set_deployment_mode --environment_id 0D2CD709-F70B-4584-A544-B209CEC8F99A --deployment_mode readonly
    ok
    ```
    * `get_deployment_mode`: for a given environment gets current deployment mode, usage:
    ``` get_deployment_mode <environment_id>```, example:
    ``` bash
    $ alertlogic-cli environment get_deployment_mode --environment_id 0D2CD709-F70B-4584-A544-B209CEC8F99A
    readonly
    ```

For further information run `alertlogic-cli --help`.