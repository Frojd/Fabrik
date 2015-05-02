# Fröjd-Fabric
A deployment toolkit built on top of Fabric.

The purpose of this library is to provide a stable python based deploy tool that covers a wide range a use cases,
Those cases include Wordpress, Node.js and Django. We favor composition and customization by code before configuration.

## Supports
- Git
- Rollbacks
- A full Django deploy script with migrations
- Virtualenv creation and activation
- NPM management
- Nginx
- Uwsgi
- Forever
- Envfile handling
- Celeryd
- Wordpress
- Composer

## Requirements
To install Frojd-Fabric you need Python 2.7, virtualenv and pip.

## Installation
Frojd-Fabric can be installed through pip.

### Stable
`pip install frojd-fabric`

### Develop
`pip install git+git://github.com/Frojd/Frojd-Fabric.git@develop`


## Project layout

We use the following project layout when deploying (it follows the same pattern as the ruby tool capistrano).

```
┌─────────────┐                            
│  releases   │─┐                          
└─────────────┘ │  ┌───────────────────┐   
                ├─▶│   201504121255    │──┐
                │  └───────────────────┘  │
                │  ┌───────────────────┐  │
                └─▶│   201504121213    │  │
                   └───────────────────┘  │
┌─────────────┐                           │
│   current   │─┬─────────────────────────┘
└─────────────┘ │  ┌───────────────────┐   
                ├─▶│     myapp.py      │   
                │  └───────────────────┘   
                │  ┌───────────────────┐   
                └─▶│      urls.py      │   
                   └───────────────────┘   
                   ┌───────────────────┐   
                   │       .env        │◀─┐
                   └───────────────────┘  │
┌─────────────┐                           │
│   shared    │─┐                         │
└─────────────┘ │  ┌──────────────────┐   │
                └─▶│       .env       │───┘
                   └──────────────────┘    
```


## Commands/tasks

|Task|Description|
|----------|:-------------:|
|setup|Initializes you application by creating the necessary directories/files. Must run first|
|deploy|Performs the actual deployment|
|rollback|Removes the current release and reactivates the previous|

```
>>> fab stage setup
>>> fab stage deploy
```


## How does it work
Frojd-Fabric consists of three parts, stages, recipes and extensions.

### Stages
The server stage is stored as a file called {stage}.py and it specifies both the recipe and some of the extensions (depending on recipe). It also defines deployment settings by both loading them from a fabricrc.txt file or hard coded in stage file.

The stages are usually placed in a folder called `envs` or `stages` and are organized like this:

```
envs
	__init__.py
	demo.py
	prod.py
```

**Example: envs/__init__.py**

The init file specifies the stages you want to activate. It might also contain stage wide settings, such as repository url.

```python
from demo import demo
from prod import prod

env.repro_url = "git@github.com:Frojd/Yourrepro.git"
```

**Example: envs/demo.py**

And here is a stage file example, this file represents the demo environment and uses the wordpress recipe.

```python
from fabric.state import env
from fabric.decorators import task
from frojd_fabric.utils import get_stage_var

@task
def demo():
	from frojd_fabric.recipes import wordpress
	
	env.stage = "demo"
	env.hosts = ["example.com"]
	env.user = "deploy"
	env.password = "password"
```

Configurations are usually loaded through a fabric settings file. Hard coded values should be avoided in most cases.

```python
	env.hosts = [get_stage_var("HOST")]
	env.user = get_stage_var("USER")
	env.password = get_stage_var("PASSWORD")
```

In the sample below `get_stage_var("USER")` will look for a parameter named `DEMO_USER` (since env.stage was named demo) in the fabricrc.txt file.

Here is a more [detailed example](https://github.com/Frojd/Frojd-Fabric/blob/develop/examples/django/fabricrc.template.txt).

### Recipes
A recipe is essentially the glue between a stage and extensions. It includes the necessary extensions and applies custom configurations that combine different extensions.

### Extensions
Is esentially a way of interacting with various server tools and software, such as nginx or uwsgi. Should be kept small, flexible and modular.

## Parameters
Frojd-Fabric requires a couple of parameters to work, the standard params (listed below) are required to any setup, while other params are depending on recipe or extension.

### Standard params

|Parameter|Description|
|----------|:-------------:|
|[hosts](http://docs.fabfile.org/en/1.10/usage/env.html#hosts)|Deployment host target|
|[user](http://docs.fabfile.org/en/1.10/usage/env.html#user)|Username|
|[password](http://docs.fabfile.org/en/1.10/usage/env.html#password)|SSH Password|
|[key_filename](http://docs.fabfile.org/en/1.10/usage/env.html#key-filename)|Absolute path to SSH key file|
|app_path|The path on the remote server where the application should be deployed (needs to be absolute)|
|source_path|If you have a subfolder you want to use as a application front (such as `src`)|
|current_path|Path where you want your latest release to be linked *(Optional)*|
|stage|The name of your deployment stage (such as `prod`)|

Here's is a [full list of the built in Fabric env vars](http://docs.fabfile.org/en/1.10/usage/env.html#environment-as-configuration)

#### Git
|Parameter|Description|
|----------|:-------------:|
|repro_url|Url to your git repro (example: `git@github.com:Frojd/Frojd-Fabric.git`|
|branch|Name of your repro branch, defaults to master *(Optional)*|

**TODO: Add more extension configurations**

## Examples
This project ships with examples for Django and Wordpress (just check `examples/*`)

## Debugging
Simple, just import `debug` from frojd_fabric.api, then run it with your command.
Debug will then generate a log file called `frojd_fabric-debug.log`.

Example: `fab debug demo deploy`


## Tests

Tests can be run with `python runtests.py`, this will run the entire suite.

It also possible to run a specific case:  `python runtests.py tests.test_api.TestApi` 

... or a specific unittest:
`test_deploy_rollback python runtests.py tests.test_api.TestApi.test_deploy_rollback`

### Writing tests

All tests should reside in the `tests` directory and prefixed `test_*`, to include a test in the main suite add the test path in `runtests.py`.


## Contributing
Want to contribute? Awesome. Just send a pull request.


## License
Frojd-Fabric is released under the [MIT License](http://www.opensource.org/licenses/MIT).

