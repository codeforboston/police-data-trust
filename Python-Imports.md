# Python Imports in Police Data Trust

# Conventions

Most code in the app runs as part of `flask`. The scraper code consists of scripts we run manually like `python foo.py` or in Jupyter notebooks. By using the same import conventions as flask in our scraper code, we can reuse code between them.

## Set `PYTHONPATH=.` and always run `python` from the repo root

Flask searches the repo root for modules; this is why absolute imports like `import backend` work in the app. To replicate this, you should run `export PYTHONPATH=.` in a shell before running `python`, and run python from the repo root. This makes python look for modules in the current working directory aka repo root. You can also add `export PYTHONPATH=.` to your shell profile. 

## Absolute paths must start at the repo root

To import the incident model from a script `backend/myscript.py` we would do `from backend.database import Incident`, rather than `from database import Incident`.

## Main script files (`foo.py` in `python foo.py`) must not use relative imports

Relative imports don’t work from the main script passed to `python`, unless `-m` is used (see 1). So it’s best to keep the main script files small and separate, so most of the code can follow flask’s import conventions.

# How Python Loads Modules

## 1. **Resolve relative imports**

Python first resolves all relative imports to absolute paths like `x.y.z`. Each module has a special `__name__` variable with the [fully-qualified name of the module](https://docs.python.org/3/reference/import.html#name__). This is like the current working directory, and relative paths are resolved by following the chain. So from a module with `__name__` of `x.y.z`, `from ..y import w` nresolves like `x/y/z/../y -> x.y`.

**However**, Python treats the main script file specially, `foo.py` in `python foo.py`. In this file, `__name__ == "__main__"`, so relative imports can’t be resolved from the main module of a script. They trigger an error:

```markdown
Traceback (most recent call last):
  File "x/y/relative.py", line 1, in <module>
    from .a import a
ImportError: attempted relative import with no known parent package
```

You *can* have python run the file as though it were imported with `-m`: `python -m foo.py`.

## 2. Find the module

Python searches the folders in `sys.path` for a module at the absolute path from 1. This includes library folders, whatever `PYTHONPATH` is set to, and the directory of the main script file.

For package imports like `x.y`, python looks for a package `x` in the `sys.path` folders, then for a module `y` in `x`'s package folder. `y` could be either a python file `y.py`  or another package. In this way, the path maps onto the filesystem. 

Python throws an error if it can’t find a module:

```markdown
Traceback (most recent call last):
  File "x/y/relative.py", line 3, in <module>
    from notamodule import a
ModuleNotFoundError: No module named 'notamodule'
```

## 3. Load the module

Finally, the code in the module is run with `__name__` set to the resolved path in step 1. All imports are