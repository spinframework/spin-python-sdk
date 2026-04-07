"""Module for interacting with a Postgres database"""

from spin_sdk.wit.imports.spin_postgres_postgres_4_2_0 import Connection

async def open(connection_string: str) -> Connection:
    """
    Open a connection with a Postgres database.
    
    The connection_string is the Postgres URL connection string.

    A `componentize_py_types.Err(Error_ConnectionFailed(str))` when a connection fails.
    
    A `componentize_py_types.Err(Error_Other(str))` when some other error occurs.
    """
    return await Connection.open_async(connection_string)
