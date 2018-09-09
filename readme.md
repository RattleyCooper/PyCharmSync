# PyCharmSync

A simple tool for uploading changed project files to a remote host,
 automatically.

Paid versions of PyCharm can be set up to upload project files
as you change them locally. `PyCharmSync` aims to do just that 
using the `sshpass` and the `scp` command on Unix based machines.

`PyCharmSync` will watch a project directory, track the files in
the directory and then upload the changed versions automatically
based on settings set in an `.env` file in your root project 
directory.

## `.env` Example

Here are some settings for a project named `project_name` on a 
raspberry pi.  The `.env` file should be consumable by `configparser.ConfigParser`

    [SSH]
    HOST = 10.0.0.200
    USER = pi
    PASS = raspberry
    PROJECT_ROOT = /home/pi/project_name

The settings laid out above would map to the following command:

    sshpass -p "PASS" scp FILEPATH USER@HOST:PROJECT_ROOT

or

    sshpass -p "raspberry" scp /home/user/project_name/some_file.py pi@10.0.0.200:/home/pi/project_name

## Usage Example

Once you have your `.env` file configured in your project's root
directory all you need to do is import `ProjectSync` from `PyCharmSync`
and then run it's `main` method:

```python
from PyCharmSync import ProjectSync

ProjectSync.main()
```

If you are not running the `main` method from your project's root 
directory you need to pass a `cwd` to the `main` method.

```python
from PyCharmSync import ProjectSync

ProjectSync.main('/home/user/project_name')
```
 
 ## Install
 
 `pip install PyCharmSync`
 