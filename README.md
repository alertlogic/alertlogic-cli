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

* Building and publishing to the PyPi

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


In order to manipulate previous releases(delete, hide, etc.) PyPi web interface to be used:
https://pypi.python.org/pypi - for the production
https://testpypi.python.org/pypi - for the testpypi


General documentation is listed here:
https://packaging.python.org/distributing/
