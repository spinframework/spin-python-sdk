# Example: `matrix-math`

This is an example of how to use [componentize-py] to build an HTTP app that
does matrix multiplication using [NumPy].  This demonstrates using a non-trivial
Python package containing native extensions within a guest component.

[componentize-py]: https://github.com/bytecodealliance/componentize-py
[NumPy]: https://numpy.org

## Prerequisites

* `spin` 4.0 or later
* `componentize-py` 0.22.0
* `NumPy`, built for WASI

Note that we use an unofficial build of NumPy since the upstream project does
not yet publish WASI builds.

```
curl -OL https://github.com/dicej/wasi-wheels/releases/download/v0.0.2/numpy-wasi.tar.gz
tar xf numpy-wasi.tar.gz
```

## Preparing the Environment

Run the following commands to setup a virtual environment with Python.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages specified in the `requirements.txt` using the command:

```bash
pip3 install -r requirements.txt
```

## Running the example

```
spin build --up
```

Then, in another terminal, send a request to the app:

```
curl -i -H 'content-type: application/json' -d '[[[1,2],[4,5],[6,7]], [[1,2,3],[4,5,6]]]' \
    http://127.0.0.1:3000/multiply
```

The output of that command should be something like:

```
HTTP/1.1 200 OK
content-type: application/json
transfer-encoding: chunked
date: Fri, 19 Jan 2024 22:24:50 GMT

[[9, 12, 15], [24, 33, 42], [34, 47, 60]]
```

If you run into any problems, please file an issue!
