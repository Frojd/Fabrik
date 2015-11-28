# How does it work
Fabrik consists of three parts, stages, recipes and extensions.

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
from fabrik.utils import get_stage_var

@task
def demo():
	from fabrik.recipes import wordpress
	
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

Here is a more [detailed example](https://github.com/Frojd/Fabrik/blob/develop/examples/django/fabricrc.template.txt).

### Recipes
A recipe is essentially the glue between a stage and extensions. It includes the necessary extensions and applies custom configurations that combine different extensions.

### Extensions
Is esentially a way of interacting with various server tools and software, such as nginx or uwsgi. Should be kept small, flexible and modular.
