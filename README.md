[Installation](share/README.md#installation)
[Configuration](share/README.md#configuration)
[Usage](share/README.md#usage)

## Tests

Additional Dependencies:

* mock
* httpretty

Running the tests:

```
cd tests
./all.py

```

## Development FAQ:

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
