"""Module for interacting with an SQLite database"""

from typing import List
from spin_sdk.wit.imports import spin_sqlite_sqlite_3_1_0 as sqlite

Connection = sqlite.Connection
Value_Integer = sqlite.Value_Integer
Value_Real = sqlite.Value_Real
Value_Text = sqlite.Value_Text
Value_Blob = sqlite.Value_Blob

async def open(name: str) -> Connection:
    """Open a connection to a named database instance.

    If `database` is "default", the default instance is opened.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_AccessDenied)` will be raised when the component does not have access to the specified database.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_NoSuchDatabase)` will be raised when the host does not recognize the database name requested.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_InvalidConnection)` will be raised when the provided connection string is not valid.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_Io(str))` will be raised when implementation-specific error occured (e.g. I/O)
    """
    return await Connection.open_async(name)

async def open_default() -> Connection:
    """Open the default store.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_AccessDenied)` will be raised when the component does not have access to the default database.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_sqlite_sqlite_3_1_0.Error_Io(str))` will be raised when implementation-specific error occured (e.g. I/O)
    """
    return await Connection.open_async("default")
