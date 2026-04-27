# A HTTP python component using componentize-py

This template uses the latest v3 version of the Spin Python SDK ([3.4.1](https://pypi.org/project/spin-sdk/3.4.1/))
for compatibility with Spin 3.x (and hosts that use this major version). The 'p2' corresponds to the wasip2 or
WASI Preview 2 set of WASI APIs, as used by Spin 3.x.

## Installing the requirements 

To build the component, [`componentize-py`](https://pypi.org/project/componentize-py/) and [`spin-sdk`](https://pypi.org/project/spin-sdk/) are required. To install them, run:

```bash
pip3 install -r requirements.txt
```

## Building and Running

```
spin up --build
```
