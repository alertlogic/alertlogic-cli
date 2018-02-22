[Installation](share/README.md#installation)
[Configuration](share/README.md#configuration)
[Usage](share/README.md#usage)

## Tests

Additional Dependencies:

* mock
* httpretty
* pytest
* pycodestyle

Running the tests:

```
make test
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
