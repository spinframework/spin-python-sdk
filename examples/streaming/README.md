# Example: Streaming with WASIp3

This is an example showcasing the use of HTTP request and response body
streaming within a guest component using WASIp3.

## Preparing the Environment

Run the following commands to setup a virtual environment with Python.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages specified in the `requirements.txt` using the
command:

```bash
pip3 install -r requirements.txt
```

## Building and Running the Examples

```bash
spin build --up
```

## Testing the App

```
curl -i -H 'content-type: text/plain' --data-binary @- http://127.0.0.1:3000/echo <<EOF
’Twas brillig, and the slithy toves
      Did gyre and gimble in the wabe:
All mimsy were the borogoves,
      And the mome raths outgrabe.
EOF
```

The above should echo the request body in the response.

In addition to the `/echo` endpoint, the app supports a `/hash-all` endpoint
which concurrently downloads one or more URLs and streams the SHA-256 hashes of
their contents.  You can test it with e.g.:

```
curl -i \
    -H 'url: https://webassembly.github.io/spec/core/' \
    -H 'url: https://www.w3.org/groups/wg/wasm/' \
    -H 'url: https://bytecodealliance.org/' \
    http://127.0.0.1:3000/hash-all
```

If you run into any problems, please file an issue!
