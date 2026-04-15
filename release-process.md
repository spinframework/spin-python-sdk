# Cutting a new release of the Spin Python SDK

To cut a new release, you will need to do the following:

1. Confirm that [CI is green](https://github.com/spinframework/spin-python-sdk/actions) for the commit selected to be tagged and released.

1. If not already bumped, set the intended release version in [pyproject.toml](./pyproject.toml), create a pull request with these changes and merge once approved.

1. Checkout the commit with the version bump from above.

1. Create and push a new tag with a `v` and then the version number.

    As an example, via the `git` CLI:

    ```
    # Create a GPG-signed and annotated tag
    git tag -s -m "Spin Python SDK v4.1.0" v4.1.0

    # Push the tag to the remote corresponding to spinframework/spin-python-sdk (here 'origin')
    git push origin v4.1.0
    ```

1. Pushing the tag upstream will trigger the [release action](https://github.com/spinframework/spin-python-sdk/actions/workflows/release.yml) which publishes the distribution to pypi.org

1. If applicable, create PR(s) or coordinate [documentation](https://github.com/spinframework/spin-docs) needs, e.g. for new features or updated functionality.