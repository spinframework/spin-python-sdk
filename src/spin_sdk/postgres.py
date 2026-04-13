"""Module for interacting with a Postgres database"""

from typing import List, Tuple, Self
from types import TracebackType
from componentize_py_types import Result
from componentize_py_async_support.streams import StreamReader
from componentize_py_async_support.futures import FutureReader
from spin_sdk.wit.imports import spin_postgres_postgres_4_2_0 as pg

RowSet = pg.RowSet
DbValue = pg.DbValue
ParameterValue = pg.ParameterValue
Column = pg.Column
Error  = pg.Error

class Connection:
    def __init__(self, connection: pg.Connection) -> None:
        self.connection = connection

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> bool | None:
        return self.connection.__exit__(exc_type, exc_value, traceback)

    @classmethod
    async def open(cls, connection_string: str) -> Self:
        """
        Open a connection with a Postgres database.

        The connection_string is the Postgres URL or connection string.

        A `componentize_py_types.Err(Error_ConnectionFailed(str))` when a connection fails.

        A `componentize_py_types.Err(Error_Other(str))` when some other error occurs.
        """
        return cls(await pg.Connection.open_async(connection_string))

    async def query(self, statement: str, params: List[ParameterValue]) -> Tuple[List[Column], StreamReader[List[DbValue]], FutureReader[Result[None, Error]]]:
        """
        Query the Postgres database.

        Returns a Tuple containing a List of Columns, a List of DbValues encapsulated in an asynchronous iterator (`componentize_py_async_support.streams.StreamReader`),
        and a future (`componentize_py_async_support.futures.FutureReader`) containing the result of the operation.

        Raises: `componentize_py_types.Err(spin_sdk.wit.imports.spin_postgres_postgres_4_2_0.Error)`
        """
        return await self.connection.query_async(statement, params)

    async def execute(self, statement: str, params: List[ParameterValue]) -> int:
        """
        Execute command to the database.

        Returns the number of affected rows as an int.

        Raises: `componentize_py_types.Err(spin_sdk.wit.imports.spin_postgres_postgres_4_2_0.Error)`
        """
        return await self.connection.execute_async(statement, params)
