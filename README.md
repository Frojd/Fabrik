# Project name
A deploy system based on Fabric, in part inspired by capistrano.

## Supports
- Git support
- Rollback
- A full Django deploy script with migrations
- Virtualenv creation and activation
- NPM management
- Nginx
- Uwsgi
- Forever
- Envfile handling
- Celeryd
- Wordpress

## Requirements
To install Frojd-Fabric you need Python 2.7, virtualenv and pip.

## Installation

Frojd-Fabric can be installed through pip.


**Develop**
`pip install git+git://github.com/Frojd/Frojd-Fabric.git@develop`

## How does it work

### Stages
A deploy script are constructed against various stages, the most common are `demo`, `dev`, `prod`. These stages are synced in your environment file against the `fabricrc.txt` settings file as a prefix.

Example: `DEMO_APP_PATH`, `LIVE_APP_PATH`

### Parameters

- General
	- HOST
	- USER
	- APP_PATH
	- APP_SOURCE_PATH

- Virtualenv
	- VENV_PATH

- UWSGI
	- UWSGI_INI_PATH

- FOREVER
    - FOREVER_APP


## Examples

This project ships with examples for Django (just check `examples/django`)

## Debugging

Simple, just import `debug` from frojd_fabric.api, then run it with your command.
Debug will then generate a log file called `frojd_fabric-debug.log`.

Example: `fab debug demo deploy`


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Frojd-Fabric is released under the [MIT License](http://www.opensource.org/licenses/MIT).

