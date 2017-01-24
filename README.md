## About:

ALCLI is a Command Line Client for Alertlogic services.

## Requirements:

1. Python 2.6+
1. Requests library

## Installation:

The easiest way to install alcli is using pip:

```pip install alcli```

## Configuration:

alcli uses only a single config file: `.config/alertlogic/auth`.
It must be an an ini style file where each section represents a profile.
Each profile has 3 fields:

* `username`: your console username
* `password`: your console password
* `datacenter`: either `uk` or `us`

Example:

``` ini
[default]
username = user@example.com
password = editme
datacenter = us
```

## Usage

alcli currently supports the following commands and subcommands:

### `environment`:
    * `set_deployment_mode`: for a given environment changes deployment mode between readonly or manual, usage:
    ``` set_deployment_mode <environment_id> <readonly|manual>```, example:
    ``` bash
    $ alcli environment set_deployment_mode 0D2CD709-F70B-4584-A544-B209CEC8F99A readonly
    ok
    ```

For further information run `alcli --help`.