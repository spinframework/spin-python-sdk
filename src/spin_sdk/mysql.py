"""Module for interacting with a MySQL database"""

from spin_sdk.wit.imports.spin_mysql_mysql_3_0_0 import Connection

async def open(connection_string: str) -> Connection:
    """
    Open a connection with a MySQL database.
    
    The connection_string is the MySQL URL connection string.

    A `componentize_py_types.Err(Error_ConnectionFailed(str))` when a connection fails.
    
    A `componentize_py_types.Err(Error_Other(str))` when some other error occurs.
    """
    return await Connection.open(connection_string)
