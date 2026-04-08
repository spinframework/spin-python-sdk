"""Module for general-purpose utility functions"""

from typing import TypeVar, Tuple, List
from componentize_py_types import Result, Err
from componentize_py_async_support.streams import StreamReader
from componentize_py_async_support.futures import FutureReader

T = TypeVar('T')
E = TypeVar('E')

async def collect(tuple: Tuple[StreamReader[T], FutureReader[Result[None, E]]]) -> List[T]:
    """
    Collect all items from the StreamReader portion of the provided Tuple and return them in a List,
    verifying the FutureReader result upon stream completion and, if it is error, raising it as an exception.
    """
    stream = tuple[0]
    future = tuple[1]
    collected = []
    with stream, future:
        while not stream.writer_dropped:
            collected += await stream.read(128)
        result = await future.read()
        if isinstance(result, Err):
            raise result
        else:
            return collected
