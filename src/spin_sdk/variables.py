"""Module for interacting with Spin Variables"""

from spin_sdk.wit.imports import fermyon_spin_variables_2_0_0 as variables

def get(key: str):
    """
    Gets the value of the given key
    """
    return variables.get(key)
