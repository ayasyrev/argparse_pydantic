# Argpare Pydantic

Config for argparse with pydantic model.

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/argparse_pydantics)](https://pypi.org/project/argparse_pydantic/)
![PyPI](https://img.shields.io/pypi/v/benchmark-utils?color=blue)  
[![Tests](https://github.com/ayasyrev/argparse_pydantic/workflows/Tests/badge.svg)](https://github.com/ayasyrev/argparse_pydantic/actions?workflow=Tests)  [![Codecov](https://codecov.io/gh/ayasyrev/argparse_pydantic/branch/main/graph/badge.svg)](https://codecov.io/gh/ayasyrev/argparse_pydantic)  

Simple wrapper for python argparse.  
Use pydantic model for you app config.  
It gives you typed config instead of default Namespace from argparse.

Tested on python 3.7 - 3.11

WIP

## Install

Install from pypi:  

`pip install argparse_pydantic`

Or install from github repo:

`pip install git+https://github.com/ayasyrev/argparse_pydantic.git`

## Base use.

We use python argparse to parse arguments from command line.  
So - just create parser as usual:


```python
import argparse

parser = argparse.ArgumentParser(prog="MyApp")
```

Than create config for you app with Pydantic.


```python
from pydantic import  BaseModel


class AppCfg(BaseModel):
    echo: str
```

Now add argument to parser from you config.


```python
from argparse_pydantic import add_args_from_model

parser = add_args_from_model(parser, AppCfg)
```

So we got parser with arguments from config.


```python
parser.print_help()
```
<details open> <summary>output</summary>  
    <pre>usage: MyApp [-h] --echo ECHO
    
    options:
      -h, --help   show this help message and exit
      --echo ECHO
    </pre>
</details>

Parse command line as usual.


```python
args = parser.parse_args(["--echo", "argument from command line"])
```

When we parse command line, we got Namespace object.  
Bat we can convert it to config object.


```python
from argparse_pydantic import create_model_obj

cfg = create_model_obj(AppCfg, args)
```

Now we got confic with type checks / validation ont type hinting when use it at IDE.


```python
cfg
```
<details open> <summary>output</summary>  
    <pre>AppCfg(echo='argument from command line')</pre>
</details>




```python
cfg.echo
```
<details open> <summary>output</summary>  
    <pre>'argument from command line'</pre>
</details>



## Examples

You can see examples at `examples` folder - Same examples as at python docs and tutorial for argparse.  
