# Pylint Env Vars

A Pylint plugin that prohibits usage of `os.environ` in certain files.

## Reasoning

There is a common django/flask pattern that advises managing project settings 
across different environments using  `base.py`, `prod.py`, `dev.py` etc.
The choice of the setting file is usually controlled by an environment variable such as `DJANGO_SETTINGS_MODULE`.
This file, in turn, relies on environment variables again, like so.:

```python
...
SECRET_KEY = os.environ['SECRET_KEY']
...

```

So, when you have settings files referencing values from environment variables,
it is dangerous to have other project files accessing `os.environ` as well: this leads to poor control over settings. Instead, these files should reference values set in the settings file:
```python
# some_obscure_module.py

key = os.environ.get('SECRET_KEY', 123)  # bad!

from django.conf import settings
key = settings.SECRET_KEY   # good

```  

Enter `pylint_env_vars`. This plugin will fail checks if your files access `os.environ` somewhere.

## Installation and Setup

```
pip install pylint_env_vars
```

Add the plugin to `[MASTER]` section of your `.pylintrc`:

```
[MASTER]
load-plugins = pylint_env_vars
```

**Add modules that can access `os.environ`, like your settings files**

Add a `[pylint_env_vars]` section to your `.pylintrc`. The arg can be a regex

```
[pylint_env_vars]
allow_in_modules = settings.*

```


The error code is `R9000`:

```
...
getmybot/settings/my.py:97: [R9000(os-environ-prohibited), ] Usage of os.environ is prohibited. Import from django settings instead.
...
```


### Some helpers

Run pylint for all `.py` files in the current dir:

```
find . -name "*.py" | xargs pylint
```

Run pylint for all `.py` files excluding some folder:

```
find . -name "*.py" | grep -v "node_modules" | xargs pylint
```



## Roadmap

Expand checks to `django-environ` library.
