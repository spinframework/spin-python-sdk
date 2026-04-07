"""Module with helpers for wasi http"""

import traceback
import componentize_py_async_support
from componentize_py_types import Ok, Result
from componentize_py_async_support.streams import ByteStreamWriter
from componentize_py_async_support.futures import FutureReader
from spin_sdk import wit
from spin_sdk.wit.imports import wasi_http_client_0_3_0_rc_2026_03_15 as client
from spin_sdk.wit.imports.wasi_http_types_0_3_0_rc_2026_03_15 import (
    Method, Method_Get, Method_Head, Method_Post, Method_Put, Method_Delete, Method_Connect,
    Method_Options, Method_Trace, Method_Patch, Method_Other,
    Fields, Scheme, Scheme_Http, Scheme_Https, Scheme_Other,  ErrorCode, Request as WasiRequest, Response as WasiResponse
)
from dataclasses import dataclass
from collections.abc import MutableMapping
from typing import Optional
from urllib import parse

@dataclass
class Request:
    """An HTTP request"""
    method: str
    uri: str
    headers: MutableMapping[str, str]
    body: Optional[bytes]

@dataclass
class Response:
    """An HTTP response"""
    status: int
    headers: MutableMapping[str, str]
    body: Optional[bytes]

try:
    from spin_sdk.wit import exports
    from spin_sdk.wit.exports import WasiHttpHandler030Rc20260315 as Base
    
    class Handler(Base):
        """Simplified handler for incoming HTTP requests using blocking, buffered I/O."""

        async def handle_request(self, request: Request) -> Response:
            """Handle an incoming HTTP request and return a response or raise an error"""
            raise NotImplementedError

        async def handle(self, request: WasiRequest) -> WasiResponse:
            method = request.get_method()

            if isinstance(method, Method_Get):
                method_str = "GET"
            elif isinstance(method, Method_Head):
                method_str = "HEAD"
            elif isinstance(method, Method_Post):
                method_str = "POST"
            elif isinstance(method, Method_Put):
                method_str = "PUT"
            elif isinstance(method, Method_Delete):
                method_str = "DELETE"
            elif isinstance(method, Method_Connect):
                method_str = "CONNECT"
            elif isinstance(method, Method_Options):
                method_str = "OPTIONS"
            elif isinstance(method, Method_Trace):
                method_str = "TRACE"
            elif isinstance(method, Method_Patch):
                method_str = "PATCH"
            elif isinstance(method, Method_Other):
                method_str = method.value
            else:
                raise AssertionError

            headers = request.get_headers().copy_all()
            request_uri = request.get_path_with_query()
            rx, trailers = WasiRequest.consume_body(request, _unit_future())
            body = bytearray()
            with rx:
                while not rx.writer_dropped:
                    body += await rx.read(16 * 1024)

            if request_uri is None:
                uri = "/"
            else:
                uri = request_uri
    
            try:
                simple_response = await self.handle_request(Request(
                    method_str,
                    uri,
                    dict(map(lambda pair: (pair[0], str(pair[1], "utf-8")), headers)),
                    bytes(body)
                ))
            except:
                traceback.print_exc()
    
                response = WasiResponse.new(Fields(), None, _trailers_future())[0]
                response.set_status_code(500)
                return response

            if simple_response.headers.get('content-length') is None:
                content_length = len(simple_response.body) if simple_response.body is not None else 0
                simple_response.headers['content-length'] = str(content_length)

            tx, rx = wit.byte_stream()
            componentize_py_async_support.spawn(_copy(simple_response.body, tx))
            response = WasiResponse.new(Fields.from_list(list(map(
                lambda pair: (pair[0], bytes(pair[1], "utf-8")),
                simple_response.headers.items()
            ))), rx, _trailers_future())[0]

            response.set_status_code(simple_response.status)
            return response

except ImportError:
    # `spin_sdk.wit.exports` won't exist if the use is targeting `spin-imports`,
    # so just skip this part
    pass

async def send(request: Request) -> Response:
    """Send an HTTP request and return a response or raise an error"""
    match request.method:
        case "GET":
            method: Method = Method_Get()
        case "HEAD":
            method = Method_Head()
        case "POST":
            method = Method_Post()
        case "PUT":
            method = Method_Put()
        case "DELETE":
            method = Method_Delete()
        case "CONNECT":
            method = Method_Connect()
        case "OPTIONS":
            method = Method_Options()
        case "TRACE":
            method = Method_Trace()
        case "PATCH":
            method = Method_Patch()
        case _:
            method = Method_Other(request.method)
    
    url_parsed = parse.urlparse(request.uri)

    match url_parsed.scheme:
        case "http":
            scheme: Scheme = Scheme_Http()
        case "https":
            scheme = Scheme_Https()
        case "":
            scheme = Scheme_Http()
        case _:
            scheme = Scheme_Other(url_parsed.scheme)

    headers_dict = request.headers

    # Add a `content-length` header if the caller didn't include one, but did
    # specify a body:
    if headers_dict.get('content-length') is None:
        content_length = len(request.body) if request.body is not None else 0
        # Make a copy rather than mutate in place, since the caller might not
        # expect us to mutate it:
        headers_dict = dict(headers_dict)
        headers_dict['content-length'] = str(content_length)

    headers = list(map(
        lambda pair: (pair[0], bytes(pair[1], "utf-8")),
        headers_dict.items()
    ))

    tx, rx = wit.byte_stream()
    componentize_py_async_support.spawn(_copy(request.body, tx))
    outgoing_request = WasiRequest.new(Fields.from_list(headers), rx, _trailers_future(), None)[0]
    outgoing_request.set_method(method)
    outgoing_request.set_scheme(scheme)
    if url_parsed.netloc == '':
        if isinstance(scheme, Scheme_Http):
            authority = ":80"
        else:
            authority = ":443"
    else:
        authority = url_parsed.netloc

    outgoing_request.set_authority(authority)

    path_and_query = url_parsed.path
    if url_parsed.query:
        path_and_query += '?' + url_parsed.query
    outgoing_request.set_path_with_query(path_and_query)

    incoming_response = await client.send(outgoing_request)

    status = incoming_response.get_status_code()
    headers = incoming_response.get_headers().copy_all()
    rx, trailers = WasiResponse.consume_body(incoming_response, _unit_future())
    body = bytearray()
    with rx:
        while not rx.writer_dropped:
            body += await rx.read(16 * 1024)

    return Response(
        status,
        dict(map(
            lambda pair: (pair[0], str(pair[1], "utf-8")),
            headers
        )),
        bytes(body)
    )

def strip_forbidden_headers(headers:MutableMapping[str, str]) -> MutableMapping[str, str]:
    """
    Strips forbidden headers for requests and responses originating from guest apps, per wasmtime/Spin
    """
    # See https://github.com/bytecodealliance/wasmtime/blob/e9e1665c5ef150d618bd8c21fb355c063596d6f7/crates/wasi-http/src/lib.rs#L42-L52
    for header in [
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "proxy-connection",
        "transfer-encoding",
        "upgrade",
        "host",
        "http2-settings"
    ]:
        try:
            del headers[header]
        except KeyError:
            pass
    return headers

async def _copy(bytes: bytes | None, tx: ByteStreamWriter) -> None:
    with tx:
        if bytes is not None:
            await tx.write_all(bytes)

def _trailers_future() -> FutureReader[Result[Optional[Fields], ErrorCode]]:
    return wit.result_option_wasi_http_types_0_3_0_rc_2026_03_15_fields_wasi_http_types_0_3_0_rc_2026_03_15_error_code_future(lambda: Ok(None))[1]

def _unit_future() -> FutureReader[Result[None, ErrorCode]]:
    return wit.result_unit_wasi_http_types_0_3_0_rc_2026_03_15_error_code_future(lambda: Ok(None))[1]
