## Getting started

### Installation

Fabrik is a python library, so first off you need to make sure you have python 2.7 installed along with pip. For handling packages we also recommend that you use virtualenv.

To install python, follow either of these guides:

- [Installing Python on Mac OS X](http://docs.python-guide.org/en/latest/starting/install/osx/)
- [Installing Python on Windows](http://docs.python-guide.org/en/latest/starting/install/win/)

To setup virtualenv, follow this guide: [Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/)


### Prepare project

Now that python is properly installed, head to your project folder to install fabrik.

1. First cd to folder: `cd ~/projects/myproject/`
1. Then setup a virtualenv called venv in your project folder: `virtualenv venv`
1. Activate the environment: `source venv/bin/activate`
1. Now time to install fabrik: `pip install fabrik`

**Requirements**

Fabrik is now installed, awesome. Now let's create the requirement files:

1. Create a directory for your requirements: `mkdir requirements`
1. Add version info: `pip freeze | grep fabrik > requirements/deploy.txt`

**Fabfile**

Time to create the fabfile.

1. `touch fabfile.py`
2. In your fabfile, add the following:

	```python
	from stages import *
	from frojd_fabric.api import setup, deploy, rollback, debug
	```

**Stages**

After that we create stubs for the various server stages (such as prod, dev)

1. `mkdir stages`
2. `cd stages`
3. `touch stage.py`
4. In the stage you just created, add something to this (this is a wordpress example):

	```python
	"""
	Example of a wordpress environment that creates a stage build.
	"""
	
	import os.path
	from fabric.state import env
	from fabric.decorators import task
	from frojd_fabric.utils import get_stage_var
	from frojd_fabric.hooks import hook
	
	
	@task
	def stage():
	    from frojd_fabric.recipes import wordpress
	
	    env.stage = "stage"
	    env.branch = "develop"
	
	    env.hosts = [get_stage_var("HOST")]
	    env.user = get_stage_var("USER")
	    env.password = get_stage_var("PASSWORD")
	    env.app_path = get_stage_var("APP_PATH")
	    env.source_path = get_stage_var("APP_SOURCE_PATH", "src")
	
	    # (Optional) Public path (example: var/www/yourproject)
	    env.public_path = get_stage_var("PUBLIC_PATH")
	```

5. Now time to let fabrik know your stage is available: `touch __init__.py`
6. Add the following:

	```python
	from fabric.state import env
	# Include all your stage environments here
	from stage import stage
	
	from frojd_fabric.transfer.git import copy
	
	
	# Put settings used by all env stages
	env.repro_url = "git@github.com:Frojd/Yourrepro.git"
	```

**Settings**

7. Almost done, now we only need to add settings. cd back to your project root: `cd ~/projects/myproject/`
8. Create a file that will hold your deployment settings: `touch fabricrc.txt`
9. Add the following (replace with your own settings):

	```bash
	STAGE_HOST=iporhosttoserver
	STAGE_USER=someuser
	STAGE_PASSWORD=somepasswordifkeyisnotused
	STAGE_KEY_FILENAME=/path/to/.ssh/id_rsa.pub
	STAGE_APP_PATH=/var/django/YOURPROJECT
	```


### Deploy

1. Before you can do a deploy you need to run a setuo command: `fabrik dev setup`
	
	This command will create the proper directories and shared files on the server (depending on your recipe). For instance a wordpress recipe will create a file called wp-config.php in the shared folder.
	
2. Now time to run a deploy: `fabrik dev deploy`. This command will create a new release with a cloned copy of the application.


### Server requirements

- git installed
- A properly configured firewall
- ssh access
- posix compatible shell
