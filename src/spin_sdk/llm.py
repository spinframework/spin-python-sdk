"""Module for working with the Spin large language model API"""

from dataclasses import dataclass
from typing import Optional, List
from spin_sdk.wit.imports import fermyon_spin_llm_2_0_0 as spin_llm


@dataclass
class InferencingParams:
    max_tokens: int = 100
    repeat_penalty: float = 1.1
    repeat_penalty_last_n_token_count: int = 64
    temperature: float = 0.8
    top_k: int = 40
    top_p: float = 0.9
    

def generate_embeddings(model: str, text: List[str]) -> spin_llm.EmbeddingsResult:
    """
    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_ModelNotSupported)` will be raised if the component does not have access to the specified model.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_RuntimeError(str))` will be raised if there are any runtime errors.

    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_InvalidInput(str))` will be raised if an invalid input is provided.
    """
    return spin_llm.generate_embeddings(model, text)

def infer_with_options(model: str, prompt: str, options: Optional[InferencingParams]) -> spin_llm.InferencingResult:
    """
    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_ModelNotSupported)` will be raised if the component does not have access to the specified model.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_RuntimeError(str))` will be raised if there are any runtime errors.

    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_InvalidInput(str))` will be raised if an invalid input is provided.
    """
    some_options = options or InferencingParams()
    my_options = spin_llm.InferencingParams(
        some_options.max_tokens,
        some_options.repeat_penalty,
        some_options.repeat_penalty_last_n_token_count,
        some_options.temperature,
        some_options.top_k,
        some_options.top_p,        
    )
    return spin_llm.infer(model, prompt, my_options)

def infer(model: str, prompt: str) -> spin_llm.InferencingResult:
    """
    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_ModelNotSupported)` will be raised if the component does not have access to the specified model.
    
    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_RuntimeError(str))` will be raised if there are any runtime errors.

    A `componentize_py_types.Err(spin_sdk.wit.imports.fermyon_spin_llm_2_0_0.Error_InvalidInput(str))` will be raised if an invalid input is provided.
    """
    return infer_with_options(model, prompt, None)

