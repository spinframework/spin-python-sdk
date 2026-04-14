  ## Building

### Prerequisites

- Python
- `pip`
- `componentize-py` 0.22.1

Once you have `pip` installed, you can install `componentize-py` using:

```bash
pip install componentize-py==0.22.1
```

### Generating the bindings

The bindings are generated from the WIT files under
[src/spin_sdk/wit](./src/spin_sdk/wit).  You can use the `regenerate_bindings.sh`
script to regenerate them:

```bash
bash regenerate_bindings.sh
```

### Updating docs

Docs are [updated automatically](.github/workflows/docs.yml) on merges to main and tag pushes.

### Building the distribution

First, make sure you have an up-to-date version of the `build` package installed:

```bash
pip install --upgrade build
```

Then, build the distribution:

```bash
rm -rf dist
python -m build
```

### Publishing the distribution

First, make sure you have an up-to-date version of the `twine` package installed:

```bash
pip install --upgrade twine
```

Then, publish the distribution:

```bash
twine upload dist/*
```

This first time you run that, it will ask for a username and password.  Enter
`__token__` for the username and specify a valid PyPI token as the password.
Contact Joel Dice for a token if you don't have one.
