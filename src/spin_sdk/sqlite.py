"""Module for interacting with an SQLite database"""

from typing import List, Tuple, Self
from types import TracebackType
from componentize_py_types import Result
from componentize_py_async_support.streams import StreamReader
from componentize_py_async_support.futures import FutureReader
from spin_sdk.wit.imports import spin_sqlite_sqlite_3_1_0 as sqlite

Error = sqlite.Error
Value = sqlite.Value
Value_Integer = sqlite.Value_Integer
Value_Real = sqlite.Value_Real
Value_Text = sqlite.Value_Text
Value_Blob = sqlite.Value_Blob
RowResult = sqlite.RowResult

class Connection:
    def __init__(self, connection: sqlite.Connection) -> None:
        self.connection = connection

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> bool | None:
        return self.connection.__exit__(exc_type, exc_value, traceback)

    @classmethod
    async def open(cls, name: str) -> Self:
        """Open a connection to a named database instance.

        If `database` is "default", the default instance is opened.

        A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_AccessDenied)` will be raised when the component does not have access to the specified database.

        A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_NoSuchDatabase)` will be raised when the host does not recognize the database name requested.

        A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_InvalidConnection)` will be raised when the provided connection string is not valid.

        A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_Io(str))` will be raised when implementation-specific error occured (e.g. I/O)
        """
        return cls(await sqlite.Connection.open_async(name))

    @classmethod
    async def open_default(cls) -> Self:
        """Open the default store.

        A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_AccessDenied)` will be raised when the component does not have access to the default database.

        A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_Io(str))` will be raised when implementation-specific error occured (e.g. I/O)
        """
        return cls(await sqlite.Connection.open_async("default"))

    async def execute(self, statement: str, params: List[Value]) -> Tuple[List[str], StreamReader[RowResult], FutureReader[Result[None, Error]]]:
        """
        Execute a command to the database.

        Returns a Tuple containing a List of columns, a List of RowResults encapsulated in an asynchronous iterator (`componentize_py_async_support.streams.StreamReader`),
        and a future (`componentize_py_async_support.futures.FutureReader`) containing the result of the operation.

        Raises: `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error)`
        """
        return await self.connection.execute_async(statement, params)

    async def last_insert_rowid(self) -> int:
        """
        The SQLite rowid of the most recent successful INSERT on the connection, or 0 if
        there has not yet been an INSERT on the connection.
        """
        return await self.connection.last_insert_rowid_async()

    async def changes(self) -> int:
        """
        The number of rows modified, inserted or deleted by the most recently completed
        INSERT, UPDATE or DELETE statement on the connection.
        """
        return await self.connection.changes_async()
