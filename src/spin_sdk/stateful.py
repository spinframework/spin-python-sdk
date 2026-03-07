"""Support for stateful Spin components.

Stateful components are long-lived, addressable Wasm components with
in-memory state and access to persistent storage. The Spin runtime manages
their lifecycle: each instance has a unique string ID, persists in-memory
state across invocations, and receives lifecycle callbacks for activation
and suspension.

Usage::

    from spin_sdk.stateful import stateful_component, Request, Response
    from spin_sdk import key_value

    @stateful_component
    class Counter:
        def __init__(self, id: str):
            self.id = id
            self.store = key_value.open_default()
            count_bytes = self.store.get(f"{id}:count")
            self.count = int(count_bytes.decode()) if count_bytes else 0

        def suspend(self):
            self.store.set(f"{self.id}:count", str(self.count).encode())

        def handle_request(self, request: Request) -> Response:
            self.count += 1
            return Response(200, {}, str(self.count).encode())

The ``@stateful_component`` decorator wires the class into the Spin runtime:

- ``__init__(self, id)`` is called when the runtime activates the instance.
  Use it to restore state from persistent storage (key-value, SQLite, etc.).
- ``suspend(self)`` is called before the runtime suspends the instance.
  Use it to flush any pending in-memory state. This method is optional.
- ``handle_request(self, request) -> Response`` handles incoming HTTP
  requests routed to this instance.  This method may be ``async def``
  to allow concurrent requests to the same instance to interleave at
  ``await`` points.

State is held as regular instance attributes on ``self`` — no locks,
guards, or special accessors are needed.
"""

import inspect
import sys
import traceback
from dataclasses import dataclass
from collections.abc import MutableMapping
from typing import Optional


@dataclass
class Request:
    """An HTTP request."""
    method: str
    uri: str
    headers: MutableMapping[str, str]
    body: Optional[bytes]


@dataclass
class Response:
    """An HTTP response."""
    status: int
    headers: MutableMapping[str, str]
    body: Optional[bytes]


_component_class = None
_component_instance = None


class _LifecycleExport:
    """WIT lifecycle export — delegates to the registered component class."""

    def instantiate(self, id: str) -> None:
        global _component_instance
        _component_instance = _component_class(id)

    def suspend(self) -> None:
        global _component_instance
        if _component_instance is not None:
            if hasattr(_component_instance, "suspend"):
                _component_instance.suspend()
            _component_instance = None


def _variant_method_to_str(method) -> str:
    """Convert a WASIp3 HTTP method variant to a string.

    componentize-py generates variant classes named Method_Get, Method_Post,
    etc. We match on the class name to avoid importing generated types.
    """
    name = type(method).__name__
    _MAP = {
        "Method_Get": "GET",
        "Method_Head": "HEAD",
        "Method_Post": "POST",
        "Method_Put": "PUT",
        "Method_Delete": "DELETE",
        "Method_Connect": "CONNECT",
        "Method_Options": "OPTIONS",
        "Method_Trace": "TRACE",
        "Method_Patch": "PATCH",
    }
    if name in _MAP:
        return _MAP[name]
    if name == "Method_Other":
        return method.value
    return "GET"


_http_types_cache = None
_world_helpers = None


def _get_http_types(request):
    """Get WASIp3 HTTP types from the request object's module.

    componentize-py generates WASIp3 types at build time in a module whose
    path varies by world. Rather than hard-coding the import path, we
    discover the types from the live request resource, which is always a
    ``wasi:http/types@0.3.0-rc-2026-01-06#request`` instance.
    """
    global _http_types_cache
    if _http_types_cache is not None:
        return _http_types_cache
    _http_types_cache = sys.modules[type(request).__module__]
    return _http_types_cache


def _get_world_helpers():
    """Discover componentize-py's stream/future helpers on the world module.

    componentize-py generates ``byte_stream()`` (for ``stream<u8>``) and a
    trailers-future constructor (for ``future<result<option<fields>,
    error-code>>``) on the world module.  The trailers-future function has
    an auto-generated name, so we find it by inspecting the module.
    """
    global _world_helpers
    if _world_helpers is not None:
        return _world_helpers

    import spin_sdk.wit as world

    byte_stream_fn = getattr(world, "byte_stream", None)

    trailers_future_fn = None
    for name in dir(world):
        if name.endswith("_future") and "fields" in name and "error_code" in name:
            trailers_future_fn = getattr(world, name)
            break

    _world_helpers = (byte_stream_fn, trailers_future_fn)
    return _world_helpers


def _make_trailers_future():
    """Create a resolved trailers future indicating no trailers and no error."""
    from componentize_py_types import Ok
    _, trailers_future_fn = _get_world_helpers()
    if trailers_future_fn is None:
        raise RuntimeError(
            "Could not find trailers-future constructor on the world module"
        )
    return trailers_future_fn(lambda: Ok(None))[1]


def _make_body_stream(body_bytes):
    """Wrap ``bytes`` in a WASIp3 ``stream<u8>`` readable end.

    Returns ``None`` for an empty body (avoiding stream overhead), or
    spawns an async writer and returns the readable end of the stream.
    """
    if not body_bytes:
        return None

    byte_stream_fn, _ = _get_world_helpers()
    if byte_stream_fn is None:
        raise RuntimeError(
            "Could not find byte_stream constructor on the world module"
        )

    tx, rx = byte_stream_fn()

    import componentize_py_async_support

    async def _write():
        with tx:
            await tx.write_all(body_bytes)

    componentize_py_async_support.spawn(_write())
    return rx


def _make_handler_class():
    """Build a Handler class that inherits the generated _async_start_handle.

    componentize-py generates ``_async_start_handle`` on the
    ``wit_world.exports.Handler`` Protocol during componentization.  We
    inherit from that class so our ``async def handle`` is wrapped
    correctly with the async start/return ABI the runtime expects.
    """
    from spin_sdk.wit.exports import Handler as _GeneratedHandler

    class _HandlerExport(_GeneratedHandler):
        async def handle(self, request):
            http_types = _get_http_types(request)

            if _component_instance is None:
                return _error_response(http_types, 503, b"Component not active")

            method_str = _variant_method_to_str(request.get_method())
            uri = request.get_path_with_query() or "/"

            headers_resource = request.get_headers()
            headers = dict(
                (name, value.decode("utf-8"))
                for name, value in headers_resource.copy_all()
            )

            body = b""

            try:
                result = _component_instance.handle_request(
                    Request(method_str, uri, headers, body)
                )
                if inspect.iscoroutine(result):
                    simple_response = await result
                else:
                    simple_response = result
            except Exception:
                traceback.print_exc()
                simple_response = Response(
                    500, {"content-type": "text/plain"}, b"Internal Server Error"
                )

            return _to_wit_response(http_types, simple_response)

    return _HandlerExport


def _error_response(http_types, status, body_bytes):
    """Build a WASIp3 response resource for error cases."""
    fields = http_types.Fields.from_list([
        ("content-type", b"text/plain"),
        ("content-length", str(len(body_bytes)).encode()),
    ])
    body_stream = _make_body_stream(body_bytes)
    response, _ = http_types.Response.new(fields, body_stream, _make_trailers_future())
    response.set_status_code(status)
    return response


def _to_wit_response(http_types, simple: Response):
    """Convert the SDK's simplified Response to a WASIp3 response resource."""
    resp_headers = simple.headers.copy()
    if resp_headers.get("content-length") is None:
        content_length = len(simple.body) if simple.body is not None else 0
        resp_headers["content-length"] = str(content_length)

    fields = http_types.Fields.from_list(
        [(k, v.encode()) for k, v in resp_headers.items()]
    )
    body_bytes = simple.body if simple.body is not None else b""
    body_stream = _make_body_stream(body_bytes)
    response, _ = http_types.Response.new(fields, body_stream, _make_trailers_future())
    response.set_status_code(simple.status)
    return response


def stateful_component(cls):
    """Register a class as a Spin stateful component.

    The decorated class should implement:

    - ``__init__(self, id: str)``: Called when the runtime activates the
      instance. ``id`` is the unique instance identifier. Restore any
      needed state from persistent storage here.
    - ``suspend(self)``: *(optional)* Called before the runtime suspends
      the instance. Flush any pending in-memory state here.
    - ``handle_request(self, request: Request) -> Response``: Handle
      incoming HTTP requests routed to this instance.
    """
    global _component_class
    _component_class = cls

    caller_module = sys.modules[cls.__module__]
    setattr(caller_module, "Lifecycle", _LifecycleExport)
    setattr(caller_module, "Handler", _make_handler_class())

    return cls
