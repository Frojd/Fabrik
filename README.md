[![Build Status](https://travis-ci.org/Frojd/Fabrik.svg?branch=master)](https://travis-ci.org/Frojd/Fabrik)
[![PyPI version](https://badge.fury.io/py/fabrik.svg)](http://badge.fury.io/py/fabrik)

![Fabrik](https://raw.githubusercontent.com/frojd/fabrik/develop/img/frojd-fabrik.png)

# Fabrik

A deployment toolkit built on top of Fabric.

The purpose of this library is to provide a stable python based deploy tool that covers a wide range a use cases,
Those cases include Wordpress, Node.js and Django. We favor composition and customization by code before configuration.

## Supports

- Git
- Rollbacks
- A full Django deploy script with migrations
- ClI for scaffolding
- Virtualenv creation and activation
- NPM management
- Nginx
- Uwsgi
- Forever
- Envfile handling
- Celeryd
- Wordpress with bedrock
- Composer
- Scp


## Requirements

To install Fabrik you need Python 2.7, virtualenv and pip.


## Installation

Fabrik can be installed through pip.

### Stable

`pip install fabrik`

### "Unstable"

- `pip install git+git://github.com/Frojd/Fabrik.git@develop`

### For development

- `git clone git@github.com:Frojd/Fabrik.git`
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install --editable .`


## Quickstart

To create setup deployment for django, run the following:
`fabrik_start --stages=stage,prod --recipe=django`

This command will create the following files.

```
/fabfile.py
/stages/
    __init__.py
    stage.py
    prod.py
```

This script will create the necessary files and add git repro setting (if present) and recipe import. Once generated, you'll need to add SSH settings and recipe unique settings by editing the files.


## Quickstart

To create setup deployment for django, run the following:
`fabrik_start --stages=stage,prod --recipe=django`

This command will create the following files.

```
/fabfile.py
/stages/
    __init__.py
    stage.py
    prod.py
```

This script will create the necessary files and add git repro setting (if present) and recipe import. Once generated, you'll need to add SSH settings and recipe unique settings by editing the files.


## Examples

This project ships with examples for Django and Wordpress (just check `examples/*`)


## Tests

Tests can be run with `python runtests.py`, this will run the entire suite. Just make sure you run `pip install -r requirements/tests.txt` first.

It also possible to run a specific case:  `python runtests.py tests.test_api.TestApi`

... or a specific unittest:
`test_deploy_rollback python runtests.py tests.test_api.TestApi.test_deploy_rollback`

### Writing tests

All tests should reside in the `tests` directory and prefixed `test_*`, to include a test in the main suite add the test path in `runtests.py`.


## Documentation

The documentation can be found [here](documentation/README.md).


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Fabrik is released under the [MIT License](http://www.opensource.org/licenses/MIT).
