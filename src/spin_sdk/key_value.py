"""Module for accessing Spin key-value stores"""

from spin_sdk.wit.imports.spin_key_value_key_value_3_0_0 import Store

async def open(name: str) -> Store:
    """
    Open the store with the specified name.
  
    If `name` is "default", the default store is opened.  Otherwise, `name` must
    refer to a store defined and configured in a runtime configuration file
    supplied with the application.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_key_value_key_value_3_0_0.Error_NoSuchStore)` will be raised if the `name` is not recognized.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_key_value_key_value_3_0_0.Error_AccessDenied)` will be raised if the requesting component does not have
    access to the specified store.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_key_value_key_value_3_0_0.Error_StoreTableFull)` will be raised if too many stores have been opened simultaneously.
    Closing one or more previously opened stores might address this using the `__exit__` method.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_key_value_key_value_3_0_0.Error_Other(str))` will be raised if some implementation specific error has occured (e.g I/O)
    """
    return await Store.open(name)

async def open_default() -> Store:
    """
    Open the default store.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_key_value_key_value_3_0_0.Error_AccessDenied)`
    will be raised if the requesting component does not have access to the
    default store.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_key_value_key_value_3_0_0.Error_StoreTableFull)` will be raised if too many stores have been opened simultaneously.
    Closing one or more previously opened stores might address this using the `__exit__` method.

    A `componentize_py_types.Err(spin_sdk.wit.imports.spin_key_value_key_value_3_0_0.Error_Other(str))` will be raised if some implementation specific error has occured (e.g I/O)
    """
    return await Store.open("default")
