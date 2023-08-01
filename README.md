# Argparse Pydantic

Config for argparse with pydantic model.

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/argparse_pydantic)](https://pypi.org/project/argparse_pydantic/)
![PyPI](https://img.shields.io/pypi/v/argparse_pydantic?color=blue)  
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
So, just create parser as usual:


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

It exactly like parser made classic way:  
`parser.add_argument("echo")`

Now we can use parser in you script usual way - `parser.parse_args()`

<!-- termynal -->
```
$ python my_app.py -h
usage: MyApp [-h] echo

positional arguments:
  echo

options:
  -h, --help  show this help message and exit
```

Parse command line as usual.


```python
args = parser.parse_args(["argument from command line"])
```

When we parse command line, we got Namespace object.  
Bat we can convert it to config object.


```python
from argparse_pydantic import create_model_obj

cfg = create_model_obj(AppCfg, args)
```

Now we got  config with type checks / validation ont type hinting when use it at IDE.


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



### Optional if undefined.

We can use undefined arguments as positional or optional (but required).


```python
class AppCfg2(BaseModel):
    arg_int: int
    arg_float: float = 0.1
```


```python
parser = argparse.ArgumentParser(prog="MyApp")
parser = add_args_from_model(parser, AppCfg2, undefined_positional=False)
```

<!-- termynal -->
```
$ python my_app.py -h
usage: MyApp [-h] --arg_int ARG_INT [--arg_float ARG_FLOAT]

options:
  -h, --help            show this help message and exit
  --arg_int ARG_INT
  --arg_float ARG_FLOAT
```

### Add types and defaults values.

And we can add type hints to help message from our config.  



```python
parser = argparse.ArgumentParser(prog="MyApp")
parser = add_args_from_model(
    parser,
    AppCfg2,
    undefined_positional=False,
    help_def_type=True,
)
```

<!-- termynal -->
```
$ python my_app.py -h
usage: MyApp [-h] --arg_int ARG_INT [--arg_float ARG_FLOAT]

options:
  -h, --help            show this help message and exit
  --arg_int ARG_INT     [int]
  --arg_float ARG_FLOAT
                        [float] default: 0.1
```

## Examples

You can see examples at `examples` folder - Same examples as at python docs and tutorial for argparse.  
