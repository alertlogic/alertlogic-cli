[Installation](share/README.md#installation)
[Configuration](share/README.md#configuration)
[Usage](share/README.md#usage)

## Tests

Additional Dependencies:

* mock
* httpretty
* pytest

Running the tests:

```
cd tests
./all.py

```

## Debugging:

* How do I run it in debug mode?

    You can set the environment variable DEBUG and then run, this will set
    logging level to `debug` and will make python load `alertlogic` lib from
    `.` instead of python's `sys.path`

    e.g:

    `$ DEBUG=yes alertlogic-cli --help`

* How can I tune logging?

    You can use any log handlers provided by the python `logging` library.
    Please see https://docs.python.org/2/library/logging.config.html#logging-config-fileformat
    to create a logging configuration file. An example of a logging
    configuration is placed to the `share/logging_config.ini.example`. This
    configuration enables two log handlers to write messages to the stream and
    to the syslog. Please provide the command line argument `--logging_config_file`
    pointing on your custom configuration file to enable your custom log handlers.


## Publishing:

In order to build, publish and test the package you need to create `~/.pypirc`:
```
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://pypi.python.org/pypi
username=alertlogic
password=password

[pypitest]
repository=https://testpypi.python.org/pypi
username=alertlogic
password=password
```

After it is created the following commands allow you to build upload and test the package:

* `make dist` - buids the package and puts it into `dist/` subfolder
* `make upload` - uploads to the `testpypi` server under alertlogic organization
* `make install` - installs the package locally(not from PyPi, to install from PyPi use pip)
* `make uninstall` - removes the package from the system
* `make register` - register the package with testpypi
* `make register_prod` - register the package with pypi
* `make upload` - build and upload version of the package to the testpypi
* `make upload_prod` - build and upload version of the package to the pypi(then can be installed as `pip install alertlogic-cli`)

In order to install the package remotely from testpypi, after it is uploaded,
use the following command:

`pip install -i https://testpypi.python.org/pypi alertlogic-cli`


In order to manipulate previous releases (delete, hide, etc.) you need to use PyPi web interface:
https://pypi.python.org/pypi - for the production
https://testpypi.python.org/pypi - for the testpypi

More info:
https://packaging.python.org/distributing/


## How to add new commands:

1. Add a subdirectory in alertlogiccli/commands/

2. Write at least 1 subcommand, they must be classes that inherit from Command
   and they must implement 2 methods:
   configure_parser() and execute()

``` python
import alertlogiccli.command
class Deploy(alertlogiccli.command.Command):
    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("deploy", help="Deploys something somewhere")
        parser.set_defaults(command=self)
    
    def execute(self, context):
        args = context.get_final_args()
        deployment = context.get_services().deployment
        response = deployment.deploy_something(account_id=args["account_id"])
        return response.http_code
```

3. in that subdirectory add an __init__.py file
   be sure to include instances of your subcommands:

``` python
from . import deployment

metadata = {
    "subcommands": [
        deployment.Deploy()
    ],
    "name": "deployment",
    "help": "deployment commands"
}
```
