[Installation](share/README.md#installation)
[Configuration](share/README.md#configuration)
[Usage](share/README.md#usage)

## Development FAQ:

* Can I use api.product.dev.alertlogic.com as endpoint? Yes, use `datacenter` = `dev` in config file
* How do I run it in debug mode? set env variable DEBUG to any value then run, this will set
  logging level to `debug` and will make python load `alertlogic` lib from `.` instead of python's `sys.path`
  e.g. `DEBUG=yes alertlogic-cli --help`
