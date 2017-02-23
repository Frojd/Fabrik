# Configuration

## Parameters
Fabrik requires a couple of parameters to work, the standard params (listed below) are required to any setup, while other params are depending on recipe or extension.

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
|public_path|A custom symlink pointing to current *(Optional)*|

Here's is a [full list of the built in Fabric env vars](http://docs.fabfile.org/en/1.10/usage/env.html#environment-as-configuration)

#### Git

|Parameter|Description|
|----------|:-------------:|
|repro_url|Url to your git repro (example: `git@github.com:Frojd/Fabrik.git`|
|branch|Name of your repro branch, defaults to master *(Optional)*|

#### SCP

|Parameter|Description|
|----------|:-------------:|
|scp_ignore_list|List of folders you wish to ignore *(Optional*)|
|local_app_path|Path you wish to copy, if not defined git root is used *(Optional*)|
