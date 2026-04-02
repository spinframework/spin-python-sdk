"""Module for utilizing Spin Outbound MQTT"""

from enum import Enum
from spin_sdk.wit.imports.spin_mqtt_mqtt_3_0_0 import Connection, Qos as Qos 

async def open(address: str, username: str, password: str, keep_alive_interval_in_secs: int) -> Connection:
    """
    Open a connection to the Mqtt instance at `address`.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_mqtt_mqtt_3_0_0.Error_InvalidAddress)` will be raised if the connection string is invalid.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_mqtt_mqtt_3_0_0.Error_TooManyConnections)` will be raised if there are too many open connections. Closing one or more previously opened connection using the `__exit__` method might help.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_mqtt_mqtt_3_0_0.Error_ConnectionFailed)` will be raised if the connection failed.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_mqtt_mqtt_3_0_0.Error_Other(str))` when some other error occurs.
    """
    return await Connection.open(address, username, password, keep_alive_interval_in_secs)
