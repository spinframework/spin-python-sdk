"""Module for interacting with Spin Variables"""

from spin_sdk.wit.imports import spin_variables_variables_3_0_0 as variables

async def get(key: str):
    """
    Gets the value of the given key
    """
    return await variables.get(key)
