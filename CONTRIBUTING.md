## Building

### Prerequisites

- Python
- `pip`
- `componentize-py` 0.25.1

Once you have `pip` installed, you can install `componentize-py` using:

```bash
pip install componentize-py==0.25.1
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

### Publishing a release

Releases are published automatically via a GitHub workflow when a version tag is
pushed to the repository.

When creating a new release, first update the the version number in the project
file, examples, templates, etc.  For example, if bumping the version from
`4.0.0` to `5.0.0`, use e.g.:

```bash
for x in $(find examples templates -name requirements.txt) README.md pyproject.toml; \
  do sed -i 's/4\.0\.0/5.0.0/' $x; \
done
```

Then run `git diff` and make sure the changes look correct, editing the result
by hand if needed.  Then open a PR to update the `main` branch.  Once that's
merged, you can create and push a release tag with the following commands
(replacing `v5.0.0` with the version you want to deploy):

```bash
git tag -s v5.0.0 -m v5.0.0
git push origin v5.0.0
```
