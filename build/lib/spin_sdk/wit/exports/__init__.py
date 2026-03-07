from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some
from ..imports import types

class InboundRedis(Protocol):

    @abstractmethod
    def handle_message(self, message: bytes) -> None:
        """
        The entrypoint for a Redis handler.
        
        Raises: `spin_sdk.wit.types.Err(spin_sdk.wit.imports.redis_types.Error)`
        """
        raise NotImplementedError


class Lifecycle(Protocol):

    @abstractmethod
    def instantiate(self, id: str) -> None:
        """
        Called once when the instance is first activated. The component
        receives its unique instance ID and should restore any needed
        state from persistent storage.
        """
        raise NotImplementedError

    @abstractmethod
    def suspend(self) -> None:
        """
        Called before the instance is suspended (idle timeout or migration).
        The component should flush any pending in-memory state to storage.
        """
        raise NotImplementedError


class IncomingHandler(Protocol):
    """WASIp2 incoming HTTP handler (wasi:http/incoming-handler@0.2.0)."""

    @abstractmethod
    def handle(self, request: types.IncomingRequest, response_out: types.ResponseOutparam) -> None:
        """
        This function is invoked with an incoming HTTP Request, and a resource
        `response-outparam` which provides the capability to reply with an HTTP
        Response. The response is sent by calling the `response-outparam.set`
        method, which allows execution to continue after the response has been
        sent. This enables both streaming to the response body, and performing other
        work.
        
        The implementor of this function must write a response to the
        `response-outparam` before returning, or else the caller will respond
        with an error on its behalf.
        """
        raise NotImplementedError


class Handler(Protocol):
    """WASIp3 HTTP handler (wasi:http/handler@0.3.0-rc-2026-01-06)."""

    @abstractmethod
    async def handle(self, request: Any) -> Any:
        """
        Handle an HTTP request and return a response.

        This is the WASIp3 handler signature. The request is a
        wasi:http/types.request resource and the return value is a
        result<response, error-code>.
        """
        raise NotImplementedError


